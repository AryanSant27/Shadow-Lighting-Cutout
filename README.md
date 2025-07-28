## Steps to run the code:

  

# 1. Clone the GitHub repository:
    

Open a new folder on your PC and open a terminal in that folder.  
Then run 

```bash

 git clone https://github.com/AryanSant27/Shadow-Lighting-Cutout.git

```

# 2. Create a virtual environment: 
    

Open the folder in an IDE and there open another terminal.  
Then type:

```bash

python -m venv venv

```

# 3. Activate Virtual Environment:
    

Once the ‘venv’ is set-up, in the terminal type:

```bash

venv\\Scripts\\activate

```

# 4. Install dependencies:
    

After activating the environment, run:

```bash

pip install -r requirements.txt 

```

This will install all the dependencies, although there are only 2 as of now so just running:

```bash 

pip install numpy cv2 

```

will also work

  

# 5. Change the assets:
    

Change the photos in the assets folder. The photo of the person needs to be a transparent PNG, this can be done by any online tool. There should be two photos in the assets folder. One being a background and the other being a transparent cut-out in .png format.

  

# 6. Run main .py:
    

Run the main file. 

  

# 7. Calculate the Sun Angle:
    

Now we need to draw a rectangle around any tall object like a tree or a lamp, if no such object is present humans will also work. The second rectangle needs to be drawn around the shadow of the object which will estimate the angle of the Sun.

  

# 8. Place the cutout in the Back-grond:
    

You can resize the cutout with the UI and place it at a suitable place in the background image.

  

# 9. Mark the Light Source:
    

In the current version, I have made it manual to mark the major light source. Although it can be automated, I was a bit short on time. Now once the source of light is marked, you will see the final output where the cutout is placed in a realistic way with a natural looking shadow.