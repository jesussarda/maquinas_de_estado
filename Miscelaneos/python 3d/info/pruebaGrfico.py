import matplotlib.pyplot as plt

# Plot a line based on the x and y axis value list.

def draw_line():

    # List to hold x values.
    x_number_values = [1, 2, 3, 4, 5]

    # List to hold y values.
    y_number_values = [1, 4, 9, 16, 25]

    # Plot the number in the list and set the line thickness.
    plt.plot(x_number_values, y_number_values, linewidth=3)

    # Set the line chart title and the text font size.
    plt.title("Square Numbers", fontsize=19)

    # Set x axes label.
    plt.xlabel("Number Value", fontsize=10)

    # Set y axes label.
    plt.ylabel("Square of Number", fontsize=10)

    # Set the x, y axis tick marks text size.
    plt.tick_params(axis='both', labelsize=9)

    # Display the plot in the matplotlib's viewer.
    plt.show()

if __name__ == '__main__':
    draw_line()