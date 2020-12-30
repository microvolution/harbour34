#include "inkey.ch"

#ifndef __HARBOUR__
#include "clipper.ch"
#endif

PROCEDURE Main()

   MEMVAR m_testvar

   LOCAL testvar

#ifdef _SET_EVENTMASK
   Set( _SET_EVENTMASK, INKEY_ALL )
   MSetCursor( .T. )
#endif

   SetKey( K_F8, {|| Recurse() } )

   CLS

   @  1, 10 PROMPT "Menu Item 1" MESSAGE "Menu Message 1"
   __AtPrompt( 2, 10, "Menu Item 2", "Menu Message 2", "R+/GR, GR+/N" )
   @  3, 10 PROMPT "Menu Item 3" MESSAGE "Menu Message 3"
   @  4, 10 PROMPT "Menu Item 4" MESSAGE "Menu Message 4"

   @  6, 10 SAY "Testing with LOCAL parameter"
   @  7, 10 SAY "Press <F8> to recurse into MENU TO"

   MENU TO testvar

   @  9, 10 SAY "Your Choice: " + hb_ntos( testvar )

   Inkey( 0 )

   SetKey( K_F8, {|| Recurse() } )

   CLS

   @  1, 10 PROMPT "Menu Item 1" MESSAGE "Menu Message 1"
   @  2, 10 PROMPT "Menu Item 2" MESSAGE "Menu Message 2"
   @  3, 10 PROMPT "Menu Item 3" MESSAGE "Menu Message 3"
   @  4, 10 PROMPT "Menu Item 4" MESSAGE "Menu Message 4"

   @  6, 10 SAY "Testing with MEMVAR parameter"
   @  7, 10 SAY "Press <F8> to recurse into MENU TO"

   MENU TO m_testvar

   @  9, 10 SAY "Your Choice: " + hb_ntos( m_testvar )

   RETURN

STATIC PROCEDURE Recurse()

   LOCAL testvar

   SetKey( K_F8, {|| Recurse() } )

   @  6, 10 SAY Space( Len( "Press <F8> to recurse into MENU TO" ) )

   @  1, 50 PROMPT "Menu Item 1" MESSAGE "Menu Message 1"
   @  2, 50 PROMPT "Menu Item 2" MESSAGE "Menu Message 2"
   @  3, 50 PROMPT "Menu Item 3" MESSAGE "Menu Message 3"
   @  4, 50 PROMPT "Menu Item 4" MESSAGE "Menu Message 4"

   MENU TO testvar

   @  7, 10 SAY "Press <F8> to recurse into MENU TO"

   @  9, 50 SAY "Your Choice: " + hb_ntos( testvar )

   SetKey( K_F8, {|| Recurse() } )

   RETURN
