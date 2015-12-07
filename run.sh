size=1100000
for dim in 4 6 8 10
do
	for delta in 0.9 0.5 0.1 0.05 0.01
	do
	   echo $dim $delta
	   python "psi_gen_refactored.py" $size $dim $delta 1
	done
done
