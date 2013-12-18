#!/usr/bin/perl

use v5.12.2;
use warnings;
use strict;

use HTML::Template;

my $t = HTML::Template->new(
  filename => q{my_template_msg.html},
);

my $msg = q{Hello World};

$t->param(message => $msg);

my $output = $t->output;

say $output;