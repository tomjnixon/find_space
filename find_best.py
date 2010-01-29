#!/usr/bin/env python
from geo import Point
import sys

class Rectangle():
    def __init__(self, top_left, bottom_right):
        self.top_left = top_left
        self.bottom_right = bottom_right
        
    @property
    def top(self):
        return self.top_left.y
    @property
    def bottom(self):
        return self.bottom_right.y
    @property
    def left(self):
        return self.top_left.x
    @property
    def right(self):
        return self.bottom_right.x

    @property
    def bottom_left(self):
        return Point(self.left, self.bottom)
    @property
    def top_right(self):
        return Point(self.right, self.top)

    @property
    def size(self):
        return self.bottom_right - self.top_left

    def point_inside(self, point):
        return (point.x < self.right and
                point.x > self.left and
                point.y > self.top and
                point.y < self.bottom)

    def intersects_with(self, other):
        return (other.top_left.x < self.bottom_right.x and
                other.top_left.y < self.bottom_right.y and
                other.bottom_right.x > self.top_left.x and
                other.bottom_right.y > self.top_left.y)


    def is_inside(self, other):
        return (self.left >= other.left and
                self.right <= other.right and
                self.top >= other.top and
                self.bottom <= other.bottom)

    @property
    def area(self):
        return self.size.x * self.size.y

    def __str__(self):
        return "R(%s,%s,%s,%s)" % (self.left, self.top, 
                                   self.right, self.bottom)

    __repr__ = __str__        

def valid_space(space):
    return space.left < space.right and space.bottom > space.top

def partition(space, window):
    if not space.intersects_with(window):
        return [space]
    else:
        spaces = []
        # left
        spaces.append(Rectangle(Point(window.right, space.top),
                                space.bottom_right))
        # top
        spaces.append(Rectangle(Point(space.left, window.bottom),
                                space.bottom_right))
        # bottom
        spaces.append(Rectangle(space.top_left,
                                Point(space.right, window.top)))
        # right
        spaces.append(Rectangle(space.top_left,
                                Point(window.left, space.bottom)))

        return filter(valid_space, spaces)


def partition_space(space, windows):
    spaces = [space]
    
    for window in windows:
        new_spaces = []
        for space in spaces:
            new_spaces.extend(partition(space, window))
        spaces = new_spaces

    return spaces

def choose_space(spaces, size):
    possible = filter(lambda space: (space.size.x >= size.x and
                                     space.size.y >= size.y    )
                      , spaces)
    if not possible:
        return None
    else:
        area = size.x * size.y
        return min(possible, key=lambda space: space.area - area)

def get_window(string):
    values = map(int, string.split(" "))

    top_left = Point(values[0], values[1])
    bottom_right = top_left + Point(values[2], values[3])
    
    return Rectangle(top_left, bottom_right)


def get_windows(f):
    return map(get_window, 
               filter(len, 
                      map(str.strip, 
                          f.readlines())))


def main():
    screen = Rectangle(Point(0,0),
                       Point(int(sys.argv[1]),
                             int(sys.argv[2])))
    size = Point(int(sys.argv[3]),
                 int(sys.argv[4]))

    windows = get_windows(sys.stdin)

    spaces = partition_space(screen, windows)

    space = choose_space(spaces, size)
    if space:
        print space.left, space.top
    else:
        sys.exit(1)

    #draw(screen, windows, spaces, Rectangle(space.top_left, space.top_left + size))

        
def draw(screen, windows, spaces, chosen_space):
    import Image, ImageDraw

    def draw_space(dc, space, **kwargs):
        dc.rectangle(((space.left, space.top),
                      (space.right, space.bottom)), **kwargs)

    im = Image.new("RGBA", list(screen.size), (255,255,255,0))
    dc = ImageDraw.Draw(im)

    for window in windows:
        draw_space(dc, window, fill=(0,255,0, 128))
        
    for space in spaces:
            draw_space(dc, space, fill=(0,0,255, 128))
    
    draw_space(dc, chosen_space, fill=(255,0,0,128))

    del dc
    im.save("test.png", "PNG")
    

if __name__ == "__main__":
    main()

