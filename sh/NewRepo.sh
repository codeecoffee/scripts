#!/bin/bash
#Author: Fellipe F Lopes 

# Add this file to .gitignore
gitignore(){
if [ -f $1.gitignore ] ;
  then echo "#Ignoring Gitscript" >> $1.gitignore 
  echo "NewRepo.sh" >> $1.gitignore
else
  echo "#Ignoring Gitscript" > $1.gitignore 
  echo "NewRepo.sh" >> $1.gitignore
fi
}

echo "This script will:\n
0. Add this file to a .gitignore file
1. Initilize a local .git
2. Add project files 
3. Commit with a message (if none the default will be applied: 'firt messge')
4. Create a public remote repo
5. Add a remote repo to master 
6. Push to master branch.\n NOTE: You must have an account on github for this to work!"

#0: Comfirmations
echo
echo "Would you like to proceed ? (Type yes or no)"
echo 
read response
if [ "$response" == "no" ] ;
  then
    exit 
fi

#1 - 2. Initilalizing and adding files...
echo "Is the path bellow the root of your project? (Type yes or no)"
path=`pwd`"/"
echo "$path"
read response

if [ "$response" == "no" ] ; 
  then
    echo "Input the exact path for your project root or end this script, copy this file into the root folder and run it again"
    read path
fi
git init
gitignore "$path"
git add $path
echo "Adding files...."

#3. Commit
message="first commit"
echo "Write a message for your commit or [press ENTER] for default message"
read message
echo "committing..."
git commit -m "$message"

#4. Creating Remote Repo
echo "Enter your github user name [press ENTER] and your reponame"
read username
read reponame

#5. Creating the public repo
echo "creating repo..."
curl -u "${username}" https://api.github.com/user/repos -d '{"name":"'"${reponame}"'", "private":false}'

#6. Pushing
echo "pushing..."
git remote add origin https://github.com/${username}/${reponame}.git
git push -u origin master
