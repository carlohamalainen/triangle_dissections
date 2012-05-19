#!/usr/bin/perl -w

@files = `ls *pdf`;

foreach $file (@files)
{
    chomp $file;
    system "cp -v $file ../output-dissections-$file";
}
