#!/bin/bash

if [[ "$1" == "-h" ]]
then
cat << EOF
$0  (command)

will start interactive shell for tag  if command empty

or

will run with the command provided 
EOF
exit 0
fi

PWD=$(pwd)
. $(dirname $0)/config.sh


case $USER in
  *vilhuber)
  WORKSPACE=$PWD
  ;;
  codespace)
  WORKSPACE=/workspaces
  ;;
esac
  
# build the docker if necessary

docker pull $space/$repo:$tag

OPTIONS="-it --rm --entrypoint /bin/bash -w /src"
# OPTIONS="-e DISABLE_AUTH=true  --rm -p 8787:8787"

docker run -v "$WORKSPACE":/src $OPTIONS $space/$repo:$tag $@
