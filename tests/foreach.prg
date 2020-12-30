PROCEDURE Main()

   LOCAL A := { "one  ", "two  ", "three" }
   LOCAL AA := { "AA-one  ", "AA-two  ", "AA-three", "AA-four " }
   LOCAL c := "abcdefghij"
   LOCAL enum := "b"
   LOCAL bb, cc
   LOCAL i

#if 0
   test( @a, b )
   test( a, @b )
   test( @a, @b )
#endif

   ? Replicate( "=", 56 )
   ? "before loop: ENUM=", ENUM
   ? "before loop: a[1]=", a[ 1 ], "a[2]=", a[ 2 ], "a[3]=", a[ 3 ]
   FOR EACH enum IN A
      ? "start: ENUM=", enum
      IF hb_LeftEq( enum, "two" )
         enum := Upper( enum )
      ENDIF
      ? "end:   ENUM=", enum, ;
         "| index:", enum:__enumIndex(), ;
         "| value:", enum:__enumValue(), ;
         "| base:", ValType( enum:__enumBase() ), ;
         "| isfirst:", enum:__enumIsFirst(), ;
         "| islast:", enum:__enumIsLast()
   NEXT
   ? "after loop ENUM=", enum
   ? "after loop: a[1]=", a[ 1 ], "a[2]=", a[ 2 ], "a[3]=", a[ 3 ]
   ? "---"
   ?
   WAIT

   ? Replicate( "=", 56 )
   ? "Testing passing by reference"
   ? "before loop: ENUM=", enum
   ? "after loop: a[1]=", a[ 1 ], "a[2]=", a[ 2 ], "a[3]=", a[ 3 ]
   FOR EACH enum IN A
      IF hb_LeftEqI( enum, "TWO" )
         enum := Upper( enum )
         ? "before passing by @ | ENUM=", enum, ;
            "| index:", enum:__enumIndex(), ;
            "| value:", enum:__enumValue(), ;
            "| base:", ValType( enum:__enumBase() ), ;
            "| isfirst:", enum:__enumIsFirst(), ;
            "| islast:", enum:__enumIsLast()
         testBYREF( @enum )
         ? " after passing by @ | ENUM=", enum, ;
            "| index:", enum:__enumIndex(), ;
            "| value:", enum:__enumValue(), ;
            "| base:", ValType( enum:__enumBase() ), ;
            "| isfirst:", enum:__enumIsFirst(), ;
            "| islast:", enum:__enumIsLast()
      ENDIF
   NEXT
   ? "after loop ENUM=", enum
   ? "after loop: a[1]=", a[ 1 ], "a[2]=", a[ 2 ], "a[3]=", a[ 3 ]
   ?
   WAIT

   ? Replicate( "=", 56 )
   ? "Testing BREAK"
   ? "before loop: ENUM=", enum
   ? "after loop: a[1]=", a[ 1 ], "a[2]=", a[ 2 ], "a[3]=", a[ 3 ]
   BEGIN SEQUENCE
      FOR EACH enum IN A DESCEND
         ? "loop:   ENUM=", enum, ;
            "| index:", enum:__enumIndex(), ;
            "| value:", enum:__enumValue(), ;
            "| base:", ValType( enum:__enumBase() ), ;
            "| isfirst:", enum:__enumIsFirst(), ;
            "| islast:", enum:__enumIsLast()
         TESTbreak( enum )
      NEXT

   RECOVER USING i
      ? "after loop ENUM=", enum
      ? "after loop: a[1]=", a[ 1 ], "a[2]=", a[ 2 ], "a[3]=", a[ 3 ]
      ? "recover variable i=", i
   END SEQUENCE
   ?
   WAIT

   ? Replicate( "=", 56 )
   ? "before loop: ENUM=", enum
   ? "before loop: c=", c
   BEGIN SEQUENCE
      FOR EACH enum IN c
         ? "start: ENUM=", enum
         IF hb_LeftEq( enum, "d" )
            enum := Upper( enum )
         ENDIF
         Testbreak( enum )
         ? "end:   ENUM=", enum, ;
            "| index:", enum:__enumIndex(), ;
            "| value:", enum:__enumValue(), ;
            "| base:", ValType( enum:__enumBase() ), ;
            "| isfirst:", enum:__enumIsFirst(), ;
            "| islast:", enum:__enumIsLast()
      NEXT
   RECOVER USING i
      ? "after loop ENUM=", enum
      ? "after loop: c=", c
      ? "recover variable i=", i
   END SEQUENCE


   ? Replicate( "=", 56 )
   FOR EACH enum, bb, cc IN A, AA, c
      ? enum, enum:__enumIndex(), enum:__enumValue()
      ? bb, bb:__enumIndex(), bb:__enumValue()
      ? cc, cc:__enumIndex(), cc:__enumValue()
   NEXT
   ?
   WAIT

   ? Replicate( "=", 56 )
   FOR EACH enum, bb, cc IN A, AA, c DESCEND
      ? enum, enum:__enumIndex(), enum:__enumValue()
      ? bb, bb:__enumIndex(), bb:__enumValue()
      ? cc, cc:__enumIndex(), cc:__enumValue()
   NEXT

   FOR EACH enum IN a
      BEGIN SEQUENCE
         IF hb_LeftEq( enum, "2" )
            BREAK
         ENDIF
      END SEQUENCE
   NEXT

   FOR EACH enum IN a
      BEGIN SEQUENCE
         IF hb_LeftEq( enum, "2" )
            ? "Breaking... enum=", enum
            BREAK enum
         ENDIF
      RECOVER USING enum
         ? "after recovery: enum=", enum
      END SEQUENCE
   NEXT

   RETURN

STATIC PROCEDURE TESTbreak( v )

   IF hb_LeftEq( v, "2" ) .OR. ;
      hb_LeftEq( v, "d" )
      ? "issuing break"
      Break( v )
   ENDIF

   RETURN

STATIC PROCEDURE TESTBYREF( enum )

   ? "start of testBYREF ENUM=", enum
   FOR EACH enum IN { 1, 2, 3 }
      ? "  -testBYREF=", enum
   NEXT
   ? "end of loop: ENUM=", enum
   enum := "22222"
   ? "end of testBYREF ENUM=", enum

   RETURN
