num := {6,8,12,9,1,0,65,7,25,78}
key := 65
found := 0
index := -1
i := 0

repeat 1 to 10 inc 1
	if num[i] = key
			found := 1
			index := i
	end
	i := i+1
end

if found = 1
	show " Found ", key, " at index ", index
end
else
	show key, " is not in this array"
end
