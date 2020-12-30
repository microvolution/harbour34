/*
 * hb_ntos() function
 *
 * Copyright 2008 Viktor Szakats (vsz.me/hb)
 * Copyright 2016 Przemyslaw Czerpak <druzus / at / priv.onet.pl>
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

#include "hbapi.h"
#include "hbapiitm.h"

HB_FUNC( HB_NTOS )
{
   PHB_ITEM pNumber = hb_param( 1, HB_IT_NUMERIC );

   if( pNumber )
   {
      char * szResult = hb_itemStr( pNumber, NULL, NULL );

      if( szResult )
      {
         HB_SIZE nToTrim = 0;

         while( szResult[ nToTrim ] == ' ' )
            ++nToTrim;

         if( nToTrim )
            memmove( szResult, szResult + nToTrim, strlen( szResult + nToTrim ) + 1 );

         hb_retc_buffer( szResult );
         return;
      }
   }

   hb_retc_null();
}

HB_FUNC( HB_NTOC )
{
   PHB_ITEM pNumber = hb_param( 1, HB_IT_NUMERIC );

   if( pNumber )
   {
      char szBuffer[ HB_MAX_DOUBLE_LENGTH ];

      if( ! HB_IS_DOUBLE( pNumber ) )
      {
         HB_MAXINT nNumber = hb_itemGetNInt( pNumber );
         int iPos = sizeof( szBuffer );
         HB_BOOL fNeg = nNumber < 0;

         if( fNeg )
            nNumber = -nNumber;
         szBuffer[ --iPos ] = '\0';
         do
         {
            szBuffer[ --iPos ] = '0' + ( char ) ( nNumber % 10 );
            nNumber /= 10;
         }
         while( nNumber != 0 );
         if( fNeg )
            szBuffer[ --iPos ] = '-';

         hb_retc( szBuffer + iPos );
      }
      else
         hb_retc( hb_dblToStr( szBuffer, sizeof( szBuffer ),
                               hb_itemGetND( pNumber ), hb_parnidef( 2, -1 ) ) );
   }
   else
      hb_retc_null();
}
