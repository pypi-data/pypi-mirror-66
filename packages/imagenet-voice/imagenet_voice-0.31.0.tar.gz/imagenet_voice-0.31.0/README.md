# ImageNet Voice
This dataset is derived from ImageNet, and contains synthetic recordings of TTS voices saying each ImageNet label 200 times. This is more or less a toy dataset, but can be very useful for projects with little-to-no data.


### Content

This dataset is currently at 28% capacity, and more will be uploaded soon. Each folder, representing a category in ImageNet, contains 200 unique TTS files generated using [ttsddg](https://pypi.org/project/ttsdg/) using the 7 pre-installed voices in OSX. 


### Acknowledgements

[pyttsx3](https://pypi.org/project/pyttsx3/) was integral to creating ttsdg. As much trouble as I had with ffmpeg and other audio libraries, pyttsx3 made it much easier than any other option I could've taken to generate this dataset.

I appreciate any help that anyone would be willing to offer to get this dataset at 100% capacity any sooner. Please contact me!

### Inspiration

I created this dataset to provide training data for a GAN that would take in an audio file of a spoken word and would generate an image of whatever was spoken. I still plan to work on that project, but I'd like to see other people perform similar tasks.
