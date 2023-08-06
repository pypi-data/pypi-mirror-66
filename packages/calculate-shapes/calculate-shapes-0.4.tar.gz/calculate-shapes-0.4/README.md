# Calculator CLI Tool

Calculator CLI tool is CLI based that calculate 2D and 3D shapes Formulas

### Setup Project
<pre>
<code>
sudo apt-get install python3-venv
git clone https://github.com/deepesh141291/calculator-cli-tool.git
cd calculator-cli-tool
python3 -m venv calc
source calc/bin/activate
python3 -m pip install --editable .
</code>
</pre>

### Help and Usage
<pre>
<code>
ubuntu@ubuntu:~/calculator-cli-tool$ calculate
Usage: calculate [OPTIONS] COMMAND [ARGS]...

Options:
  -d      Print debug messages to stdout.
  --help  Show this message and exit.

Commands:
  circle     List of operations performed on circle.
  cube       List of operations performed on Cube.
  rectangle  List of operations performed on rectangle.
  sphere     List of operations performed on sphere.
  square     List of operations performed on square.


ubuntu@ubuntu:~/calculator-cli-tool$ calculate rectangle --help
Click Version: 7.1.1
Python Version: 3.6.9 (default, Nov  7 2019, 10:44:02)
[GCC 8.3.0]
Usage: calculate rectangle [OPTIONS] WIDTH HEIGHT

  List of operations performed on rectangle.

Options:
  -o, --operation TEXT  List of Operation Performed are ['area', 'perimeter']
                        [required]

  --help                Show this message and exit.
</code>
</pre>

### Calculate 2D shapes Opearions Area and Perimeter

ubuntu@ubuntu:~/calculator-cli-tool$ calculate circle -o area 10

Formula of Circle area = 3.14xradiusxradius
Circle area= 314.000000

### Calculate 3D shapes Opearions SurfaceArea and Volume

ubuntu@ubuntu:~/calculator-cli-tool$ calculate sphere -o volume 10

Formula of Sphere volume = (4/3)xpixradiusxradiusxradius
Sphere volume= 4188.790205

ubuntu@ubuntu:~/calculator-cli-tool$ calculate cone -o surfacearea 10 12.2
Click Version: 7.1.1
Python Version: 3.6.9 (default, Nov  7 2019, 10:44:02)
[GCC 8.3.0]
Formula of Cones surfacearea = pixradius(radius+sqrt(radiusxradius+heightxheight))



