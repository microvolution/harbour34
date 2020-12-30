/*
 * Video subsystem for plain ANSI C stream IO
 *
 * Copyright 1999-2016 Viktor Szakats (vsz.me/hb)
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2, or (at your option)
 * any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; see the file LICENSE.txt.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
 * Boston, MA 02110-1301 USA (or visit https://www.gnu.org/licenses/).
 *
 * As a special exception, the Harbour Project gives permission for
 * additional uses of the text contained in its release of Harbour.
 *
 * The exception is that, if you link the Harbour libraries with other
 * files to produce an executable, this does not by itself cause the
 * resulting executable to be covered by the GNU General Public License.
 * Your use of that executable is in no way restricted on account of
 * linking the Harbour library code into it.
 *
 * This exception does not however invalidate any other reasons why
 * the executable file might be covered by the GNU General Public License.
 *
 * This exception applies only to the code released by the Harbour
 * Project under the name Harbour.  If you copy code from other
 * Harbour Project or Free Software Foundation releases into a copy of
 * Harbour, as the General Public License permits, the exception does
 * not apply to the code that you add in this way.  To avoid misleading
 * anyone as to the status of such modified files, you must delete
 * this exception notice from them.
 *
 * If you write modifications of your own for Harbour, it is your choice
 * whether to permit this exception to apply to your modifications.
 * If you do not wish that, delete this exception notice.
 *
 */

/* NOTE: User programs should never call this layer directly! */

#define HB_GT_NAME  CGI

/*
 * HB_GT_CGI_RAWOUTPUT controls the behavior of GTCGI output
 * When not set GT driver output data in Refresh()/Redraw() methods
 * from super GT memory buffer - it causes that columns are wrapped
 * after last col.
 * It changes the previous behavior though it gives some improvements
 * like enabling DispBegin()/DispEnd() for output buffering.
 * If it's wrong and someone will prefer the old GTCGI behavior then
 * please uncomment HB_GT_CGI_RAWOUTPUT macro what will cause that
 * WriteCon(), Write(), WriteAt() method will be overload by GTCGI
 * and output data send directly without any buffering and line wrapping.
 */


#define HB_GT_CGI_RAWOUTPUT

#include "hbapi.h"
#include "hbgtcore.h"
#include "hbinit.h"
#include "hbapifs.h"
#include "hbapicdp.h"
#include "hbdate.h"

#if defined( HB_OS_WIN ) && ! defined( HB_OS_WIN_CE )
   #define HB_GT_CGI_WIN
   #include <windows.h>
   #include "hbwinuni.h"
#endif

static int s_GtId;
static HB_GT_FUNCS SuperTable;
#define HB_GTSUPER   ( &SuperTable )
#define HB_GTID_PTR  ( &s_GtId )

#define HB_GTCGI_GET( p )  ( ( PHB_GTCGI ) HB_GTLOCAL( p ) )

typedef struct _HB_GTCGI
{
   PHB_GT         pGT;        /* core GT pointer */
   HB_FHANDLE     hStdout;
   int            iRow;
   int            iCol;
   int            iLastCol;
#ifndef HB_GT_CGI_RAWOUTPUT
   int            iLineBufSize;
   char *         sLineBuf;
#endif
   char *         szCrLf;
   HB_SIZE        nCrLf;
#ifdef HB_GT_CGI_WIN
   HB_BOOL        fIsConsole;
#endif
} HB_GTCGI, * PHB_GTCGI;

#ifdef HB_GT_CGI_WIN
static HANDLE DosToWinHandle( HB_FHANDLE fHandle )
{
   switch( fHandle )
   {
      case ( HB_FHANDLE ) FS_ERROR:
         return NULL;
      case ( HB_FHANDLE ) HB_STDIN_HANDLE:
         return GetStdHandle( STD_INPUT_HANDLE );
      case ( HB_FHANDLE ) HB_STDOUT_HANDLE:
         return GetStdHandle( STD_OUTPUT_HANDLE );
      case ( HB_FHANDLE ) HB_STDERR_HANDLE:
         return GetStdHandle( STD_ERROR_HANDLE );
   }
   return ( HANDLE ) fHandle;
}
#endif

static void hb_gt_cgi_termOut( PHB_GTCGI pGTCGI, const char * szStr, HB_SIZE nLen )
{
#ifdef HB_GT_CGI_WIN
   #define HB_WIN_IOWRITE_LIMIT  10000  /* https://tahoe-lafs.org/trac/tahoe-lafs/ticket/1232#no1 */

   if( pGTCGI->fIsConsole )
   {
      HANDLE hFile = DosToWinHandle( pGTCGI->hStdout );

      HB_SIZE nWritten = 0;
      HB_SIZE nCount;

      LPTSTR lpString;

#if defined( UNICODE )
      lpString = hb_cdpnStrDupU16( HB_GTSELF_TERMCP( pGTCGI->pGT ),
                                   HB_CDP_ENDIAN_NATIVE,
                                   szStr, nLen, &nCount );
#else
      nCount = nLen;
      lpString = hb_cdpnDup( szStr, &nCount,
                             HB_GTSELF_TERMCP( pGTCGI->pGT ), hb_setGetOSCP() );
#endif

      while( nCount )
      {
         DWORD dwToWrite;
         DWORD dwWritten;

         /* Determine how much to write this time */
         if( nCount > ( HB_SIZE ) HB_WIN_IOWRITE_LIMIT )
         {
            dwToWrite = HB_WIN_IOWRITE_LIMIT;
            nCount -= ( HB_SIZE ) dwToWrite;
         }
         else
         {
            dwToWrite = ( DWORD ) nCount;
            nCount = 0;
         }

         if( ! WriteConsole( hFile, lpString + nWritten,
                             dwToWrite, &dwWritten, NULL ) )
            break;

         nWritten += ( HB_SIZE ) dwWritten;

         if( dwWritten != dwToWrite )
            break;
      }

      hb_xfree( lpString );
   }
   else
      hb_fsWriteLarge( pGTCGI->hStdout, szStr, nLen );
#else
   hb_fsWriteLarge( pGTCGI->hStdout, szStr, nLen );
#endif
}

static void hb_gt_cgi_newLine( PHB_GTCGI pGTCGI )
{
   hb_gt_cgi_termOut( pGTCGI, pGTCGI->szCrLf, pGTCGI->nCrLf );
}

static void hb_gt_cgi_Init( PHB_GT pGT, HB_FHANDLE hFilenoStdin, HB_FHANDLE hFilenoStdout, HB_FHANDLE hFilenoStderr )
{
   PHB_GTCGI pGTCGI;

   HB_TRACE( HB_TR_DEBUG, ( "hb_gt_cgi_Init(%p,%p,%p,%p)", ( void * ) pGT, ( void * ) ( HB_PTRUINT ) hFilenoStdin, ( void * ) ( HB_PTRUINT ) hFilenoStdout, ( void * ) ( HB_PTRUINT ) hFilenoStderr ) );

   HB_GTLOCAL( pGT ) = pGTCGI = ( PHB_GTCGI ) hb_xgrabz( sizeof( HB_GTCGI ) );

   pGTCGI->pGT = pGT;
   pGTCGI->hStdout = hFilenoStdout;

   pGTCGI->szCrLf = hb_strdup( hb_conNewLine() );
   pGTCGI->nCrLf = strlen( pGTCGI->szCrLf );

#ifdef HB_GT_CGI_WIN
   {
      DWORD dwMode;
      pGTCGI->fIsConsole = GetConsoleMode( DosToWinHandle( pGTCGI->hStdout ), &dwMode );
      if( pGTCGI->fIsConsole )
         HB_GTSELF_SETDISPCP( pGT, "UTF8", NULL, HB_FALSE );
   }
#endif

   hb_fsSetDevMode( pGTCGI->hStdout, FD_BINARY );

   HB_GTSUPER_INIT( pGT, hFilenoStdin, hFilenoStdout, hFilenoStderr );
   HB_GTSELF_SETFLAG( pGT, HB_GTI_STDOUTCON, HB_TRUE );
}

static void hb_gt_cgi_Exit( PHB_GT pGT )
{
   PHB_GTCGI pGTCGI;

   HB_TRACE( HB_TR_DEBUG, ( "hb_gt_cgi_Exit(%p)", ( void * ) pGT ) );

   HB_GTSELF_REFRESH( pGT );

   pGTCGI = HB_GTCGI_GET( pGT );

   HB_GTSUPER_EXIT( pGT );

   if( pGTCGI )
   {
      /* update cursor position on exit */
      if( pGTCGI->iLastCol > 0 )
         hb_gt_cgi_newLine( pGTCGI );

#ifndef HB_GT_CGI_RAWOUTPUT
      if( pGTCGI->iLineBufSize > 0 )
         hb_xfree( pGTCGI->sLineBuf );
#endif
      if( pGTCGI->szCrLf )
         hb_xfree( pGTCGI->szCrLf );
      hb_xfree( pGTCGI );
   }
}

static int hb_gt_cgi_ReadKey( PHB_GT pGT, int iEventMask )
{
   HB_TRACE( HB_TR_DEBUG, ( "hb_gt_cgi_ReadKey(%p,%d)", ( void * ) pGT, iEventMask ) );

   HB_SYMBOL_UNUSED( pGT );
   HB_SYMBOL_UNUSED( iEventMask );

   return 13;
}

static HB_BOOL hb_gt_cgi_IsColor( PHB_GT pGT )
{
   HB_TRACE( HB_TR_DEBUG, ( "hb_gt_cgi_IsColor(%p)", ( void * ) pGT ) );

   HB_SYMBOL_UNUSED( pGT );

   return HB_FALSE;
}

static void hb_gt_cgi_Bell( PHB_GT pGT )
{
   static const char s_szBell[] = { HB_CHAR_BEL, 0 };
   PHB_GTCGI pGTCGI;

   HB_TRACE( HB_TR_DEBUG, ( "hb_gt_cgi_Bell(%p)", ( void * ) pGT ) );

   pGTCGI = HB_GTCGI_GET( pGT );

   hb_gt_cgi_termOut( pGTCGI, s_szBell, 1 );
}

static const char * hb_gt_cgi_Version( PHB_GT pGT, int iType )
{
   HB_TRACE( HB_TR_DEBUG, ( "hb_gt_cgi_Version(%p,%d)", ( void * ) pGT, iType ) );

   HB_SYMBOL_UNUSED( pGT );

   if( iType == 0 )
      return HB_GT_DRVNAME( HB_GT_NAME );

   return "Terminal: Raw stream I/O (CGI)";
}

static void hb_gt_cgi_Scroll( PHB_GT pGT, int iTop, int iLeft, int iBottom, int iRight,
                              int iColor, HB_USHORT usChar, int iRows, int iCols )
{
   int iHeight, iWidth;

   HB_TRACE( HB_TR_DEBUG, ( "hb_gt_cgi_Scroll(%p,%d,%d,%d,%d,%d,%d,%d,%d)", ( void * ) pGT, iTop, iLeft, iBottom, iRight, iColor, usChar, iRows, iCols ) );

   /* Provide some basic scroll support for full screen */
   HB_GTSELF_GETSIZE( pGT, &iHeight, &iWidth );
   if( iCols == 0 && iRows > 0 &&
       iTop == 0 && iLeft == 0 &&
       iBottom >= iHeight - 1 && iRight >= iWidth - 1 )
   {
      PHB_GTCGI pGTCGI = HB_GTCGI_GET( pGT );

      /* scroll up the internal screen buffer */
      HB_GTSELF_SCROLLUP( pGT, iRows, iColor, usChar );
      /* update our internal row position */
      pGTCGI->iRow -= iRows;
      if( pGTCGI->iRow < 0 )
         pGTCGI->iRow = 0;
      pGTCGI->iLastCol = pGTCGI->iCol = 0;
   }
   else
      HB_GTSUPER_SCROLL( pGT, iTop, iLeft, iBottom, iRight, iColor, usChar, iRows, iCols );
}

#ifdef HB_GT_CGI_RAWOUTPUT
static void hb_gt_cgi_conPos( PHB_GTCGI pGTCGI, int iRow, int iCol )
{
   int iLineFeed = 0, iSpace = 0;

   if( pGTCGI->iRow != iRow )
   {
      iLineFeed = pGTCGI->iRow < iRow ? iRow - pGTCGI->iRow : 1;
   }
   else if( pGTCGI->iCol > iCol )
   {
      iLineFeed = 1;
      iSpace = iCol;
   }
   else if( pGTCGI->iCol < iCol )
   {
      iSpace = iCol - pGTCGI->iCol;
   }

   if( iSpace > 0 )
   {
      char * buffer = ( char * ) hb_xgrab( iSpace );
      memset( buffer, ' ', iSpace );
      hb_gt_cgi_termOut( pGTCGI, buffer, iSpace );
      hb_xfree( buffer );
   }
   while( --iLineFeed >= 0 )
      hb_gt_cgi_newLine( pGTCGI );
   pGTCGI->iRow = iRow;
   pGTCGI->iCol = iCol;

}

static void hb_gt_cgi_conOut( PHB_GT pGT, const char * szText, HB_SIZE nLength,
                              PHB_CODEPAGE cdpHost, PHB_CODEPAGE cdpTerm )
{
   PHB_GTCGI pGTCGI = HB_GTCGI_GET( pGT );

   if( cdpTerm && cdpHost && cdpTerm != cdpHost )
   {
      HB_SIZE nLen = nLength, nBufSize = 0;
      char * pBuf = NULL;
      const char * buffer = hb_cdpnDup3( szText, nLen,
                                         NULL, &nLen,
                                         &pBuf, &nBufSize,
                                         cdpHost, cdpTerm );
      hb_gt_cgi_termOut( pGTCGI, buffer, nLen );
      if( pBuf )
         hb_xfree( pBuf );
   }
   else
      hb_gt_cgi_termOut( pGTCGI, szText, nLength );

   while( nLength-- )
   {
      switch( *szText++ )
      {
         case HB_CHAR_BEL:
            break;

         case HB_CHAR_BS:
            if( pGTCGI->iCol )
               pGTCGI->iCol--;
            break;

         case HB_CHAR_LF:
            pGTCGI->iRow++;
            break;

         case HB_CHAR_CR:
            pGTCGI->iCol = 0;
            break;

         default:
            ++pGTCGI->iCol;
      }
   }
   HB_GTSUPER_SETPOS( pGT, pGTCGI->iRow, pGTCGI->iCol );
}

static void hb_gt_cgi_WriteCon( PHB_GT pGT, const char * szText, HB_SIZE nLength )
{
   hb_gt_cgi_conOut( pGT, szText, nLength, HB_GTSELF_HOSTCP( pGT ), HB_GTSELF_TERMCP( pGT ) );
}

static void hb_gt_cgi_WriteConW( PHB_GT pGT, const HB_WCHAR * szTextW, HB_SIZE nLength )
{
   PHB_CODEPAGE cdpTerm = HB_GTSELF_TERMCP( pGT );
   HB_SIZE nSize = hb_cdpU16AsStrLen( cdpTerm, szTextW, nLength, 0 );
   char * buffer = ( char * ) hb_xgrab( nSize );

   hb_cdpU16ToStr( cdpTerm, HB_CDP_ENDIAN_NATIVE, szTextW, nLength, buffer, nSize );
   hb_gt_cgi_conOut( pGT, buffer, nSize, NULL, NULL );
   hb_xfree( buffer );
}

static void hb_gt_cgi_WriteAt( PHB_GT pGT, int iRow, int iCol, const char * szText, HB_SIZE nLength )
{
   hb_gt_cgi_conPos( HB_GTCGI_GET( pGT ), iRow, iCol );
   hb_gt_cgi_WriteCon( pGT, szText, nLength );
}

static void hb_gt_cgi_WriteAtW( PHB_GT pGT, int iRow, int iCol, const HB_WCHAR * szTextW, HB_SIZE nLength )
{
   PHB_CODEPAGE cdpTerm = HB_GTSELF_TERMCP( pGT );
   HB_SIZE nSize = hb_cdpU16AsStrLen( cdpTerm, szTextW, nLength, 0 );
   char * buffer = ( char * ) hb_xgrab( nSize );

   hb_cdpU16ToStr( cdpTerm, HB_CDP_ENDIAN_NATIVE, szTextW, nLength, buffer, nSize );
   hb_gt_cgi_conPos( HB_GTCGI_GET( pGT ), iRow, iCol );
   hb_gt_cgi_conOut( pGT, buffer, nSize, NULL, NULL );
   hb_xfree( buffer );
}

#else /* HB_GT_CGI_RAWOUTPUT */

static void hb_gt_cgi_Redraw( PHB_GT pGT, int iRow, int iCol, int iSize )
{
   int iColor;
   HB_BYTE bAttr;
   HB_USHORT usChar;
   int iLineFeed, iHeight, iWidth, iLen;
   PHB_GTCGI pGTCGI;

   HB_TRACE( HB_TR_DEBUG, ( "hb_gt_cgi_Redraw(%p,%d,%d,%d)", ( void * ) pGT, iRow, iCol, iSize ) );

   pGTCGI = HB_GTCGI_GET( pGT );
   HB_GTSELF_GETSIZE( pGT, &iHeight, &iWidth );
   iLineFeed = iLen = 0;

   if( pGTCGI->iRow != iRow )
   {
      iLineFeed = pGTCGI->iRow < iRow ? iRow - pGTCGI->iRow : 1;
      pGTCGI->iLastCol = pGTCGI->iCol = iCol = 0;
      iSize = iWidth;
   }
   else if( pGTCGI->iCol < iCol )
   {
      iSize += iCol - pGTCGI->iCol;
      iCol = pGTCGI->iCol;
   }
   else if( pGTCGI->iCol > iCol )
   {
      iLineFeed = 1;
      iCol = pGTCGI->iCol = pGTCGI->iLastCol = 0;
      iSize = iWidth;
   }

   while( iSize > 0 && iCol + iSize > pGTCGI->iLastCol &&
          HB_GTSELF_GETSCRCHAR( pGT, iRow, iCol + iSize - 1, &iColor, &bAttr, &usChar ) )
   {
      if( usChar != ' ' )
         break;
      --iSize;
   }

   if( iSize > 0 )
   {
      PHB_CODEPAGE cdpTerm = HB_GTSELF_TERMCP( pGT );
      int iIndex = 0;

      while( --iLineFeed >= 0 )
         hb_gt_cgi_newLine( pGTCGI );
      pGTCGI->iRow = iRow;

      while( iLen < iSize )
      {
         if( ! HB_GTSELF_GETSCRCHAR( pGT, iRow, iCol, &iColor, &bAttr, &usChar ) )
            break;
         iIndex += ( int ) hb_cdpTextPutU16( cdpTerm, pGTCGI->sLineBuf + iIndex,
                                                      pGTCGI->iLineBufSize - iIndex, usChar );
         ++iLen;
         ++iCol;
      }
      if( iIndex )
      {
         hb_gt_cgi_termOut( pGTCGI, pGTCGI->sLineBuf, iIndex );
         pGTCGI->iCol = iCol;
         if( pGTCGI->iCol > pGTCGI->iLastCol )
            pGTCGI->iLastCol = pGTCGI->iCol;
      }
   }
}

static void hb_gt_cgi_Refresh( PHB_GT pGT )
{
   int iHeight, iWidth;
   PHB_GTCGI pGTCGI;

   HB_TRACE( HB_TR_DEBUG, ( "hb_gt_cgi_Refresh(%p)", ( void * ) pGT ) );

   pGTCGI = HB_GTCGI_GET( pGT );
   HB_GTSELF_GETSIZE( pGT, &iHeight, &iWidth );
   iWidth *= HB_MAX_CHAR_LEN;
   if( pGTCGI->iLineBufSize < iWidth )
   {
      pGTCGI->sLineBuf = ( char * ) hb_xrealloc( pGTCGI->sLineBuf, iWidth );
      pGTCGI->iLineBufSize = iWidth;
   }
   HB_GTSUPER_REFRESH( pGT );
}

#endif /* HB_GT_CGI_RAWOUTPUT */

/* *********************************************************************** */

static HB_BOOL hb_gt_FuncInit( PHB_GT_FUNCS pFuncTable )
{
   HB_TRACE( HB_TR_DEBUG, ( "hb_gt_FuncInit(%p)", ( void * ) pFuncTable ) );

   pFuncTable->Init                       = hb_gt_cgi_Init;
   pFuncTable->Exit                       = hb_gt_cgi_Exit;
   pFuncTable->IsColor                    = hb_gt_cgi_IsColor;
#ifdef HB_GT_CGI_RAWOUTPUT
   pFuncTable->WriteCon                   = hb_gt_cgi_WriteCon;
   pFuncTable->WriteConW                  = hb_gt_cgi_WriteConW;
   pFuncTable->Write                      = hb_gt_cgi_WriteCon;
   pFuncTable->WriteW                     = hb_gt_cgi_WriteConW;
   pFuncTable->WriteAt                    = hb_gt_cgi_WriteAt;
   pFuncTable->WriteAtW                   = hb_gt_cgi_WriteAtW;
#else
   pFuncTable->Redraw                     = hb_gt_cgi_Redraw;
   pFuncTable->Refresh                    = hb_gt_cgi_Refresh;
#endif
   pFuncTable->Scroll                     = hb_gt_cgi_Scroll;
   pFuncTable->Version                    = hb_gt_cgi_Version;
   pFuncTable->Bell                       = hb_gt_cgi_Bell;

   pFuncTable->ReadKey                    = hb_gt_cgi_ReadKey;

   return HB_TRUE;
}

/* *********************************************************************** */

#include "hbgtreg.h"

/* *********************************************************************** */
