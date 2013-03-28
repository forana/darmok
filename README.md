darmok
==========
Simple python utility for generating data models for name generation from a list of names. Can also use this model to generate names.

Named after a certain TNG episode.

Usages
----------

darmok.py train &lt;input file&gt; &lt;output file&gt;

Builds up a data model using the input file and writes it as JSON to the output file.

Example:
	darmok.py train names.txt names.json

darmok.py generate &lt;input file&gt; [&lt;minimum length&gt; [&lt;maximum length&gt; [&lt;count&gt;]]]

Using the data model represented in the input file to generate one or more names.
The names will be a minimum of 3 characters long, unless another is specified.
The names will be a maximum of 32 characters long, unless another is specified.
By default 1 will be generated, unless count is specified.

Example:
	darmok.py generate names.json 2 12 5

darmok.py help

Shows this message.