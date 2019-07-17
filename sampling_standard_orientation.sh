#! /bin/bash

echo $#

# this code searches standard orientation from the bottom line of file and prints out the cartecian coordinate.

if [ $# -eq 0 ]; then

     echo   Usage: print-standard mol.log
     echo this code searches standard orientation from the bottom line  of file and print the cartecian coordinate.

     exit

fi

str=$(tac $1 |  grep -n "Standard orientation:" $1 |  tail -n 1 |  awk '{print $1}' )

#str=$(grep -n "Standard orientation:" $1   tail -n 1   awk '{print $1}' )

start=$(echo "${str//:}")

end=$(wc -l $1 |  awk '{print $1}')

#echo $end

end=$(sed ''"$start"','"$end"'!d' $1 |  nl -ba -v$start |  grep "\-\-\-\-\-" |   head -n 3 | tail -n 1  | awk '{print $1}')

#echo $end

N=$(echo $end-$start-5|  bc)

echo $N

echo " " 

#sed ''"$(echo $start+5  bc)"','"$(echo $end-1 bc)"'!d' $1   awk '{print $2,$4,$5,$6}' | sed -e 's/^1 / H /g' -e 's/^6 / C /g' -e 's/^7 / N /g' -e 's/^8 / O /g' -e 's/^16 / S /g' -e 's/^26 / Fe /g' 

#sed ''"$(echo $start+5 | bc)"','"$(echo $end-1| bc)"'!d' $1 |  awk '{print $2,$4,$5,$6}' 

sed ''"$(echo $start+5 | bc)"','"$(echo $end-1| bc)"'!d' $1 |  awk '{print $2,$4,$5,$6}' | sed -e   's/^1 /  H  /g'  -e   's/^2 /  He  /g'   -e   's/^3 /  Li  /g'   -e   's/^4 /  m  /g'   -e   's/^5 /  B  /g'   -e   's/^6 /  C  /g'   -e   's/^7 /  N  /g'   -e   's/^8 /  O  /g'   -e   's/^9 /  F  /g'   -e   's/^10 /  Ne  /g'   -e   's/^11 /  Na  /g'   -e   's/^12 /  Mg  /g'   -e   's/^13 /  Al  /g'   -e   's/^14 /  Si  /g'   -e   's/^15 /  us  /g'   -e   's/^16 /  S  /g'   -e   's/^17 /  Cl  /g'   -e   's/^18 /  Ar  /g'   -e   's/^19 /  K  /g'   -e   's/^20 /  Ca  /g'   -e   's/^21 /  Sc  /g'   -e   's/^22 /  Ti  /g'   -e   's/^23 /  V  /g'   -e   's/^24 /  Cr  /g'   -e   's/^25 /  Mn  /g'   -e   's/^26 /  Fe  /g'   -e   's/^27 /  Co  /g'   -e   's/^28 /  Ni  /g'   -e   's/^29 /  Cu  /g'   -e   's/^30 /  Zn  /g'   -e   's/^31 /  Ga  /g'   -e   's/^32 /  Ge  /g'   -e   's/^33 /  As  /g'   -e   's/^34 /  Se  /g'   -e   's/^35 /  Br  /g'   -e   's/^36 /  Kr  /g'   -e   's/^37 /  Rb  /g'   -e   's/^38 /  Sr  /g'   -e   's/^39 /  Y  /g'   -e   's/^40 /  Zr  /g'   -e   's/^41 /  Nb  /g'   -e   's/^42 /  Mo  /g'   -e   's/^43 /  Tc  /g'   -e   's/^44 /  Ru  /g'   -e   's/^45 /  Rh  /g'   -e   's/^46 /  Pd  /g'   -e   's/^47 /  Ag  /g'   -e   's/^48 /  Cd  /g'  -e   's/^49 /  In  /g'  -e   's/^50 /  Sn  /g'  -e   's/^51 /  Sb  /g'  -e   's/^52 /  Te  /g'  -e   's/^53 /  I  /g'  -e   's/^54 /  Xe  /g'  -e   's/^55 /  Cs  /g'  -e   's/^56 /  Ba  /g'  -e   's/^57 /  La  /g'  -e   's/^58 /  Ce  /g'  -e   's/^59 /  Pr  /g'  -e   's/^60 /  Nd  /g'  -e   's/^61 /  Pm  /g'  -e   's/^62 /  Sm  /g'  -e   's/^63 /  Eu  /g'  -e   's/^64 /  um  /g'  -e   's/^65 /  Tb  /g'  -e   's/^66 /  Dy  /g'  -e   's/^67 /  Ho  /g'  -e   's/^68 /  Er  /g'  -e   's/^69 /  Tm  /g'  -e   's/^70 /  Yb  /g'  -e   's/^71 /  Lu  /g'  -e   's/^72 /  Hf  /g'  -e   's/^73 /  Ta  /g'  -e   's/^74 /  W  /g'  -e   's/^75 /  Re  /g'  -e   's/^76 /  Os  /g'  -e   's/^77 /  Ir  /g'  -e   's/^78 /  Pt  /g'  -e   's/^79 /  Au  /g'  -e   's/^80 /  Hg  /g'  -e   's/^81 /  Tl  /g'  -e   's/^82 /  Pb  /g'  -e   's/^83 /  Bi  /g'  -e   's/^84 /  Po  /g'  -e   's/^85 /  At  /g'  -e   's/^86 /  Rn  /g'  -e   's/^87 /  Fr  /g'  -e   's/^88 /  Ra  /g'  -e   's/^89 /  Ac  /g'  -e   's/^90 /  Th  /g'  -e   's/^91 /  Pa  /g'  -e   's/^92 /  U  /g'  -e   's/^93 /  Np  /g'  -e   's/^94 /  Pu  /g'  -e   's/^95 /  Am  /g'  -e   's/^96 /  Cm  /g' -e   's/^97 /  Bk  /g'  -e   's/^98 /  Cf  /g'  -e   's/^99 /  Es  /g'  -e   's/^100 /  Fm  /g'  -e   's/^101 /  Md  /g'  -e   's/^102 /  No  /g'  -e   's/^103 /  Lr  /g'  -e   's/^104 /  Rf  /g'  -e   's/^105 /  Db  /g'  -e   's/^106 /  Sg  /g'  -e   's/^107 /  Bh  /g'  -e   's/^108 /  Hs  /g'  -e   's/^109 /  Mt  /g'
