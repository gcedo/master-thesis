// Copyright Nominet UK 2013
// Written by Roy Arends

#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
   const char *t[] = {"com", "net", "biz", "ru", "org", "co.uk", "info"};
   unsigned int d, i, m, s, y, z;
   char n[16];

   if (argc != 4)
   {
       printf ("usage: %s d m y\n", argv[0]);
   }
   else
   {
      for (z = 0; z < 1000; z++)
      {
         d = atoi(argv[1]);
         m = atoi(argv[2]);
         y = atoi(argv[3]) + z;

         d *= 65537;
         m *= 65537;
         y *= 65537;

         s = d>>3 ^ y>>8 ^ y>>11;
         s &= 3;
         s += 12;

         for(i = 0; i < s; i++)
         {
             d = d<<13>>19 ^ d>>1<<13 ^ d>>19;
             m = m<<2>>25  ^ m>>3<<7  ^ m>>25;
             y = y<<3>>11  ^ y>>4<<21 ^ y>>11;
             n[i] = 'a' + ( y ^ m ^ d ) % 25;
         }
         n[i]=0;
         printf("%s.%s\n", n, t[z%7]);
      }
   }
}