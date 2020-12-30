/* Copyright 2000 Luiz Rafael Culik <Culik@sl.conex.net>
   See LICENSE.txt for licensing terms. */

#include "hbapi.h"

#if defined( HB_OS_DOS )
   #include <dos.h>
#endif

/* https://www.delorie.com/djgpp/doc/rbinter/ix/33/00.html */

HB_FUNC( _FT_MSETSENSITIVE )  /* nHoriz, nVert, nDouble */
{
#if defined( HB_OS_DOS )
   {
      union REGS regs;
      regs.HB_XREGS.ax = 0x1A;
      regs.HB_XREGS.bx = hb_parni( 1 );
      regs.HB_XREGS.cx = hb_parni( 2 );
      regs.HB_XREGS.dx = hb_parni( 3 );
      HB_DOS_INT86( 0x33, &regs, &regs );
   }
#endif
}

HB_FUNC( FT_MGETSENS )
{
   int iHoriz;
   int iVert;
   int iDouble;

#if defined( HB_OS_DOS )
   {
      union REGS regs;
      regs.HB_XREGS.ax = 0x1B;
      HB_DOS_INT86( 0x33, &regs, &regs );
      iHoriz  = regs.HB_XREGS.bx;
      iVert   = regs.HB_XREGS.cx;
      iDouble = regs.HB_XREGS.dx;
   }
#else
   iHoriz  = 0;
   iVert   = 0;
   iDouble = 0;
#endif

   hb_storni( iHoriz, 1 );
   hb_storni( iVert, 2 );
   hb_storni( iDouble, 3 );
}

HB_FUNC( FT_MCONOFF )
{
#if defined( HB_OS_DOS )
   {
      union REGS regs;
      regs.HB_XREGS.ax = 0x1A;
      regs.HB_XREGS.cx = hb_parni( 2 ) * 8;  /* nLeft */
      regs.HB_XREGS.dx = hb_parni( 1 ) * 8;  /* nTop */
      regs.HB_XREGS.si = hb_parni( 4 ) * 8;  /* nRight */
      regs.HB_XREGS.di = hb_parni( 3 ) * 8;  /* nBottom */
      HB_DOS_INT86( 0x33, &regs, &regs );
   }
#endif
}

HB_FUNC( FT_MBUTPRS )
{
   int inX;
   int inY;
   int inButton;
   int iStatus;

#if defined( HB_OS_DOS )
   {
      union REGS regs;
      regs.HB_XREGS.ax = 5;
      regs.HB_XREGS.bx = hb_parni( 1 );
      HB_DOS_INT86( 0x33, &regs, &regs );
      inX      = regs.HB_XREGS.dx;
      inY      = regs.HB_XREGS.cx;
      inButton = regs.HB_XREGS.bx;
      iStatus  = regs.HB_XREGS.ax;
   }
#else
   inX      = 0;
   inY      = 0;
   inButton = 0;
   iStatus  = 0;
#endif

   hb_storni( inButton, 2 );
   hb_storni( inX, 3 );
   hb_storni( inY, 4 );

   hb_retni( iStatus );
}

HB_FUNC( FT_MBUTREL )
{
   int inX;
   int inY;
   int inButton;
   int iStatus;

#if defined( HB_OS_DOS )
   {
      union REGS regs;
      regs.HB_XREGS.ax = 6;
      regs.HB_XREGS.bx = hb_parni( 1 );
      HB_DOS_INT86( 0x33, &regs, &regs );
      inX      = regs.HB_XREGS.dx;
      inY      = regs.HB_XREGS.cx;
      inButton = regs.HB_XREGS.bx;
      iStatus  = regs.HB_XREGS.ax;
   }
#else
   inX      = 0;
   inY      = 0;
   inButton = 0;
   iStatus  = 0;
#endif

   hb_storni( inButton, 2 );
   hb_storni( inX, 3 );
   hb_storni( inY, 4 );

   hb_retni( iStatus );
}

HB_FUNC( FT_MDEFCRS )
{
#if defined( HB_OS_DOS )
   {
      union REGS regs;
      regs.HB_XREGS.ax = 10;
      regs.HB_XREGS.bx = hb_parni( 1 );  /* nCurType */
      regs.HB_XREGS.cx = hb_parni( 2 );  /* nScrMask */
      regs.HB_XREGS.dx = hb_parni( 3 );  /* nCurMask */
      HB_DOS_INT86( 0x33, &regs, &regs );
   }
#endif
}
