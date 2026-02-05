#include <graphics.h>
#include <conio.h>
#include <stdlib.h>
#include <stdio.h>
#include <dos.h> // For delay function

void drawClockFace(int radius) {
    // Draw the clock face
    circle(300, 300, radius);
    for (int i = 0; i < 12; i++) {
        int angle = i * 30; // 30 degrees for each hour
        int x = 300 + radius * cos(angle * 3.14 / 180);
        int y = 300 - radius * sin(angle * 3.14 / 180);
        line(300, 300, x, y);
    }
}

void drawHand(int angle, int length, int thickness, int color) {
    // Draw the clock hand
    setcolor(color);
    int x = 300 + length * cos(angle * 3.14 / 180);
    int y = 300 - length * sin(angle * 3.14 / 180);
    setlinestyle(SOLID_LINE, 0, thickness);
    line(300, 300, x, y);
}

void displayTime(int seconds) {
    // Calculate hours, minutes, and seconds
    int hours = seconds / 3600;
    int minutes = (seconds % 3600) / 60;
    seconds = seconds % 60;

    char timeString[9];
    sprintf(timeString, "%02d:%02d:%02d", hours, minutes, seconds);
    
    // Display the time in the center of the clock
    setcolor(WHITE);
    outtextxy(250, 280, timeString);
}

int main() {
    int gd = DETECT, gm;
    initgraph(&gd, &gm, "C:\\Turboc3\\BGI"); // Adjust path as necessary

    int totalTime;
    printf("Enter the total time for the countdown (in seconds): ");
    scanf("%d", &totalTime);

    // Draw the clock face
    drawClockFace(150);

    for (int i = totalTime; i >= 0; i--) {
        // Clear the previous time display
        setcolor(BLACK);
        outtextxy(250, 280, "        "); // Clear previous time

        // Update the clock hands
        int secondAngle = (i % 60) * 6; // 360 degrees / 60 seconds
        int minuteAngle = ((i / 60) % 60) * 6; // 360 degrees / 60 minutes
        int hourAngle = ((i / 3600) % 12) * 30; // 360 degrees / 12 hours

        // Draw the hands
        drawHand(secondAngle, 120, 1, RED);
        drawHand(minuteAngle, 100, 2, GREEN);
        drawHand(hourAngle, 80, 3, BLUE);

        // Display the time
        displayTime(i);

        delay(1000); // Wait for 1 second
        // Clear hands for the next iteration
        setcolor(BLACK);
        drawHand(secondAngle, 120, 1, BLACK);
        drawHand(minuteAngle, 100, 2, BLACK);
        drawHand(hourAngle, 80, 3, BLACK);
    }

    // Final message
    setcolor(WHITE);
    outtextxy(250, 280, "Time's up!");
    getch(); // Wait for a key press
    closegraph();
    return 0;
}
