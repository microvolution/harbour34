// Testing array functions: AIns(), ADel(), ASize(), AFill()

#ifndef __HARBOUR__
#include "clipper.ch"
#endif

PROCEDURE Main()

   LOCAL aFirst
   LOCAL aSecond
   LOCAL aMore

   aFirst := AClone( { 1, 2, 4 } )
   AIns( aFirst, 3 )
   aFirst[ 3 ] := "3"
   ? "Testing AIns() ... "
   ADump( aFirst )

   aSecond := { 1, 2, 4 }
   ASize( aSecond, 4 )
   ? "Testing ASize() ... "
   ADump( aSecond )

   aSecond := { 1, 2, 4 }
   ASize( aSecond, 4 )
   AIns( aSecond, 3 )
   aSecond[ 3 ] := "3"
   ? "Testing ASize() + AIns() ... "
   ADump( aSecond )

   aSecond := { 1, 2, 3, 3, 4, 5 }
   ADel( aSecond, 3 )
   ? "Testing ADel() ... "
   ADump( aSecond )

   aSecond := { 1, 2, 3, 3, 4, 5 }
   ADel( aSecond, 3 )
   ASize( aSecond, Len( aSecond ) - 1 )
   ? "Testing ASize() + ADel() ... "
   ADump( aSecond )

   AFill( aSecond, "!" )
   ? "Testing AFill() ... "
   ADump( aSecond )

   aMore := { 1, 2, 3, 4, 5, 6 }
   AFill( aMore, "X", 3 )
   ? "Testing AFill() with start ... "
   ADump( aMore )

   aMore := { 1, 2, 3, 4, 5, 6 }
   AFill( aMore, "X", 3, 2 )
   ? "Testing AFill() with start and count ... "
   ADump( aMore )

   aMore := { { 1, 2 }, { 3, 4 } }
   ADel( aMore, 1 )
   ADump( aMore )

   RETURN

STATIC PROCEDURE ADump( aShow )

   LOCAL tmp

   ?? "Len =", hb_ntos( Len( aShow ) )
   ?? ": "
   FOR tmp := 1 TO Len( aShow )

      ?? "["
      ?? hb_ntos( tmp )
      ?? "] = "
      ?? ValType( aShow[ tmp ] )
      ?? ":"
      IF HB_ISARRAY( aShow[ tmp ] )  /* Iterate array */
         ?
         ?? "["
         ADump( aShow[ tmp ] )
         ?? "]"
      ELSE
         ?? iif( HB_ISNUMERIC( aShow[ tmp ] ), hb_ntos( aShow[ tmp ] ), aShow[ tmp ] )
      ENDIF

      IF tmp < Len( aShow )
         ?? ", "
      ENDIF
   NEXT

   RETURN
