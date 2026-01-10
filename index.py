import numpy as np
import matplotlib.pyplot as plt

students=np.array(["Rishab","Hardik","Dakshesh","Vishnu"])
marks=np.array([70,60,55,87])

plt.bar(students,marks)

plt.xlabel("Student")
plt.ylabel("marks")

plt.title("Students Marks")

plt.show()