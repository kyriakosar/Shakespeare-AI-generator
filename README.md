# Computational Creativity - Bad Poets Society


## Brief Description
This project shows how a Shakespeare-like poem can be generated using four phases. In the first phase, we gather Shakespeare's poems and bring them in the format we want through preprocessing. Following that, we build a poem generator. The technique we use is combining N-grams, where N=3. Afterwards, we validate the quality of the poem by checking whether four specific properties of Shakespeare's sonnets appear in the generated poem. Lastly, we present the poem using generative AI so as to generate the desired background and fonts and produce text-to-audio transformation. 


## Files
- requirements.txt: It saves a list of the modules and packages required for our project. Note: the whole project was implemented in a new virtual environment and therefore it contains only the required modules and packages for the purpose of the project with NO additional useless packages.

- poem_scraper.py: A python script that is able to retrieve poems for our inspiration dataset. It has two values: "topic" and "artist". Based on them, it either retrieves poems for a specific topic (through the Poem Hunter website) or poems for a specific artist (through the PoetryDB website) 

- scraper_results_joy.txt: An example of a file containing collected poems from the Poem Hunter website regarding the topic joy.

- scraper_results_Shakespeare.txt: An example of a file containing collected poems from the PoetryDB website regarding the artist Shakespeare.

- preprocessing.py: When yoy have a retrieved file of poems in a directory with the name "data", you can run this script to output the preprocessed version of that file. It removes some metadata and puncuations marks and adds tokens at the end of each line to declare the end of the corresponging lyric.  

- poembuilder.py: A python script that is able to produce n-grams of a given collection of poems (after they have been preprocessed with the above preprocessing.py script). In this file, we generate poems with the proposed technique of connecting n-grams.

- poem_generator_markov.ipynb: A jupyter file that is able to generate poems of a given collection of poems (after they have been preprocessed with the above preprocessing.py script).

- poem_evaluation.ipynb: A jupyter file for evaluating a generated poem. This is done based on four selected properties of Shakespeare's poems: 14 lines (3 stanzas and 1 couplet), rhyming scheme, 10 syllables and iambic pentameter. 

- create.py: It is used for visualization process. In particular, it makes the papyrus background. All the operations use the OpenAI API.  

- GenerateImage.ipynb: It is also used for visualization process. In particular, it makes the appropriate fonts for the papyrus background. Actually, it merges the text and the background image.

## How to run 
- Get the modules for the project:    
    - pip install -r requirements.txt

- Get a file with Shakespeare poems:
    - python poem_scraper.py

- Get a preprocessed file of the above you downloaded:
    - python preprocessing.py

- Generate a poem:
    - python poembuilder.py


## License
MIT License
