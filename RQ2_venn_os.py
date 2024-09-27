import matplotlib.pyplot as plt
from matplotlib_venn import venn2

# Define the sets
set_a = {
    "UNIX", "Red Hat", "FreeBSD", "SUSE", "BSD", "BlackBerry", "Ubuntu", 
    "HP-UX", "OpenVMS", "IBM AIX", "IBM z/OS", "Red Hat Enterprise Linux", 
    "Windows 8"
}
set_b = {
    "professional x64", "Windows Server 2019"
}

# Define the intersection
intersection = {
    "Android", "Apple Mac", "Apple iOS", "Chrome OS", "Linux", "Solaris", 
    "Unknown", "Windows", "Windows 10", "Windows 7", "Windows 8.1", 
    "Windows Server", "Windows Server 2003", "Windows Server 2008", 
    "Windows Server 2012", "Windows Server 2016", "Windows Vista", "Windows XP"
}

# Add the intersection to both sets
set_a.update(intersection)
set_b.update(intersection)

# Calculate the unique elements in set A and set B
set_a_unique = set_a - set_b
set_b_unique = set_b - set_a

# Create the Venn diagram with equal-sized circles
plt.figure(figsize=(10, 8))
# Set equal size for both sets manually
equal_size = max(len(set_a_unique), len(set_b_unique), len(intersection))

v = venn2(subsets=(equal_size, equal_size, len(intersection)), 
          set_labels=('NCSC', 'APT'), alpha=0.5)

# Set the colors of the Venn diagram
v.get_patch_by_id('10').set_facecolor('#1f77b4')  # default blue from matplotlib
v.get_patch_by_id('01').set_facecolor('#007acc')  # more blue
v.get_patch_by_id('11').set_facecolor('skyblue')  # sky blue

# Add the operating systems to the Venn diagram
label = v.get_label_by_id('10')
label.set_text('\n'.join(set_a_unique))
label.set_fontsize(9)  # Reduce the font size

label = v.get_label_by_id('01')
label.set_text('\n'.join(set_b_unique))
label.set_fontsize(9)  # Reduce the font size

label = v.get_label_by_id('11')
label.set_text('\n'.join(intersection))
label.set_fontsize(9)  # Reduce the font size

# Show the plot
plt.show()

