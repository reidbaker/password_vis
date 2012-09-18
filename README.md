[1]: https://github.com/atizo/PyTagCloud        "PyTagCloud"
[2]: http://en.wikipedia.org/wiki/List_of_British_words_not_widely_used_in_the_United_States "Wikipedia"

This uses [PyTagCloud][1] to create a word cloud from python dictionarys.
Cloud choices include password leaks from yahoo and billabong and myspace
and a list of british words not used in the united states.
British words come from [Wikipedia][2]


To run first install [PyTagCloud][1] 
Then clone Repo
>`git clone https://github.com/reidbaker/password_vis.git`

Then run vis.py
>`python vis.py`
This generates a the word cloud with a transparent background to be used later
If your list of words is too large you may get an error about not being able to read the font correctly

Then run portrait_words.py with your image of choice
>`python portrait_words.py -f image.jpg`



Inspired by http://layersmagazine.com/photoshop-cs4-a-picture-worth-a-thousand-words.html
