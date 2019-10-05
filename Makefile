
clean:
	rm -rf build

install:
	mkdir /usr/lib/micropython/rubikscubesolvermicropython/
	cp rubikscubesolvermicropython/*.py /usr/lib/micropython/rubikscubesolvermicropython/
	cp rubikscubesolvermicropython/*.txt /usr/lib/micropython/rubikscubesolvermicropython/
