IP="34.200.233.215"

(cat ./collisions.txt; cat -) | ncat "$IP" 27490
