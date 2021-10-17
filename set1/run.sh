for i in $(ls | grep "c[0-9]*\.py");
do
	PYTHONPATH=../ python $i
	if [ $? != "0" ];
	then
		echo "FAILED ON $i"
		exit $?
	fi
done
echo "SUCCESS!!"