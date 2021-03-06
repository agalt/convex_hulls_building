
import matplotlib.pyplot as plt
import time

def reduction(points_arr):
    len_arr = len(points_arr)
    for i in range(1, len_arr):
        if points_arr[i][0] < points_arr[0][0]:
            points_arr[i], points_arr[0] = points_arr[0], points_arr[i]

def rotate(A, B, C):
    return (B[0] - A[0]) * (C[1] - B[1]) - (B[1] - A[1]) * (C[0] - B[0])

def calculate_figure_area(hull):
    s = 0.0
    lh = len(hull)
    for i in range(lh):
        s += hull[i][0] * hull[(i + 1)%lh][1] - hull[i][1] * hull[(i + 1)%lh][0]
    return abs(s * 1/2)

def hull_building(points_arr):
     hull = [points_arr[0]]
     points_arr.append(points_arr.pop(0))
     l = len(points_arr)

     while True:
         l = len(points_arr)
         right = 0
         for i in range(1, l):
             if rotate(hull[-1], points_arr[right], points_arr[i]) < 0:
                 right = i
         if points_arr[right] == hull[0]:
             points_arr.pop(right)
             break
         else:
             hull.append(points_arr[right])
             points_arr.pop(right)


# Выявление и удаление точек из массива, которые лежат на выпуклой оболочке
     lh = len(hull)
     j = 0
     while j != (len(points_arr)):
         for i in range(lh):
             if rotate(hull[i], hull[(i + 1) % lh], points_arr[j]) == 0:
                 points_arr.pop(j)
                 j -= 1
                 break
         j += 1

     return hull


def drow_points(points_arr):
    lp = len(points_arr)
    x = [points_arr[i][0] for i in range(lp)]
    y = [points_arr[i][1] for i in range(lp)]
    plt.scatter(x, y, marker = 'o')

def draw_hull(hull):
    lh = len(hull)
    x = [hull[i][0] for i in range(lh)]
    x.append(x[0])
    y = [hull[i][1] for i in range(lh)]
    y.append(y[0])
    plt.plot(x,
             y)

def spectr(filename):
    data = open(filename, 'r').read().split()
    data.pop(0)
    points_arr = []

    for i in range(0, len(data), 2):
        points_arr.append([float(data[i]), float(data[i + 1])])

    reduction(points_arr)
    drow_points(points_arr)

    spectr = []
    k = 0

    while True:
        hull = hull_building(points_arr)
        draw_hull(hull)
        spectr.append([k, calculate_figure_area(hull)])
        if len(points_arr) == 0:
            break
        if len(points_arr) < 2:
            spectr.append([k+1, 0.0])
            break



        reduction(points_arr)
        k += 1

    plt.show()
    return spectr
start = time.time()
filename_holder = open('name_input_file.txt', 'r').read().split()
filename = 'data/' + str(filename_holder[0])
Spectr = spectr(filename)

output = open('output.txt', 'w')
output.write(str(filename_holder[0]) + '\n' + "Всего оболочек: " + str(len(Spectr)) + '\n')# + '\n' + str(Spectr))
for i in Spectr:
    output.write('(' + str(i[0]) + ', ' + str(i[1]) + ')' + '\n')

output.close()
end = time.time()
print(end - start)