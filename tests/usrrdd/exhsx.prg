#include "dbinfo.ch"

PROCEDURE Main()

   FIELD FIRST, LAST, STREET, CITY
   LOCAL n, hs

   rddSetDefault( "HSCDX" )

   dbCreate( "_tst.dbf", { ;
      { "FIRST",       "C", 20,  0 }, ;
      { "LAST",        "C", 20,  0 }, ;
      { "STREET",      "C", 30,  0 }, ;
      { "CITY",        "C", 30,  0 }, ;
      { "STATE",       "C",  2,  0 }, ;
      { "ZIP",         "C", 10,  0 }, ;
      { "HIREDATE",    "D",  8,  0 }, ;
      { "MARRIED",     "L",  1,  0 }, ;
      { "AGE",         "N",  2,  0 }, ;
      { "SALARY",      "N",  6,  0 }, ;
      { "NOTES",       "C", 70,  0 } } )
   USE _tst.dbf
   hsx_Create( "_tst.hsx", "FIRST+LAST+STREET+CITY", 2, 0, .T., 3 )
   APPEND FROM ( hb_DirSepToOS( "..\test.dbf" ) )

   /* Look for all records which have 'SHERMAN' string inside */
   hs := hsx_Handle( "_tst" )
   hs_Set( hs, "SHERMAN" )
   DO WHILE ( n := hs_Next( hs ) ) > 0
      dbGoto( n )
      IF hs_Verify( hs ) > 0
         ? RTrim( FIRST + LAST + STREET + CITY )
      ENDIF
   ENDDO
   WAIT

   /* Does RDD support Record Map Filters? */
   IF dbInfo( DBI_RM_SUPPORTED )
      /* if yest then let set filter for all records with 'SHERMAN'
         word and look at them in browser */
      hs_Filter( hs, "SHERMAN" )
      dbGoTop()
      Browse()
   ENDIF

   RETURN
