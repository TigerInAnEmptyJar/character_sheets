# /bin/bash

progress_bar() {
    local elapsed=$1
    local nbars=$2
    local bars_to_draw=$(($elapsed*$nbars/$total)) 
    local previous_bars=$((($elapsed-1)*$nbars/$total))

    already_done() { for ((done=0; done<$bars_to_draw; done++)); do printf "#"; done }
    remaining() { for ((remain=$bars_to_draw; remain<$nbars; remain++)); do printf " "; done }
    percentage() { printf "| %s%%" $(( (($elapsed)*100)/($total)*100/100 )); }
    clean_line() { printf "\r"; }

  if [ $previous_bars != $bars_to_draw ] ; then
  already_done; remaining; percentage
  clean_line
  fi
}

python generate_character.py

echo "Testing for '$1'"

total=$(ls -1q generated_data/$1.json | wc -l)
echo "Number of tests: $total"
files=generated_data/$1.json

i=0
mkdir -p $(pwd)/done
mkdir -p $(pwd)/done/generated_data/
for f in $files; do
    python ../dnd2tex.py "$(pwd)/$f" --outfile "$(pwd)/done/$f.pdf" &>> "$(pwd)/test.log"
    if [ $? != 0 ] ; then
        echo "Unsuccessful $f"
        exit 1
    fi
    ((i=i+1))
    progress_bar $i 100
done
printf "\n" 