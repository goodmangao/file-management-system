# -*- coding:utf-8 -*-
"""
作者：hang
日期：2021年11月30日
"""


class File:
    owner = "default"  # File's owner is 'default '

    def chown(self, owner):  # Change the owner
        self.owner = owner


class PlainFile(File):
    class_name = "PlainFile"  # PlainFile's name

    def __init__(self, name):  # initialization
        self.name = name

    def __str__(self):  # Turn an instance of a class into str format
        return self.name

    def ls(self, num=0):  # output current file name and owner
        print(" " * num + f"{self.name}({self.owner})")


class Directory(File):
    class_name = 'Directory'  # Directory's name

    def __init__(self, name, contents, owner=None):
        self.name = name
        self.contents = contents
        if owner:
            self.chown(owner)

    def __str__(self):
        # print Directory recursively
        ret = ""
        files = []
        for file in self.files:
            files += [str(file)]

        join = ""
        for item in files:
            if not join:
                join = str(item)
            else:
                join += ", " + str(item)

        ret += f"{self.class_name}({self.name}, [{join}])"
        return ret

    def ls(self, num=0):
        # print Directory in tree structure with indentation to indicate the num
        print(" " * num + f"{self.name}({self.owner})")
        num += 4
        for file in self.contents:
            file.ls(num)


# navigate and manipulate a file system as if it was a UNIX file system
class FileSystem:
    def __init__(self, name):
        self.catalog = name  # All catalog
        self.cdl = name  # Current directory location
        self.elder = []

    def pwd(self):
        return self.cdl.name  # Return current working directory

    # List contents under current directory
    def ls(self):
        return self.cdl.ls()

    # Modify the method cd() to allow us to go back to a parent directory.
    def cd(self, new_dir):
        if new_dir == "..":
            if self.catalog == self.cdl:
                return
            self.cdl = self.elder[-1]
            self.elder = self.elder[:-1]
            return
        for file in self.cdl.contents:
            if file.name == new_dir and file.class_name == "Directory":
                self.elder = self.elder + [self.cdl]
                self.cdl = file
                return
        print("The directory does not exist!")

    # Create new PlainFile under current directory if it does not already exist.
    def create_file(self, name):
        pf_name = []
        for file in self.cdl.contents:  # Find all file names in the directory(contents)
            if file.class_name == "PlainFile":
                pf_name = pf_name + [file.name]
        if name in pf_name:  # It is already exist
            print("The file already exists!")
            return
        new_pl = PlainFile(name)
        new_pl.chown(self.cdl.owner)
        self.cdl.contents = self.cdl.contents + [new_pl]  # add new directory

    # Create new directory under current directory if it does not already exist and owner can be specified.
    def mkdir(self, name, owner=None):
        dir_name = []
        for file in self.cdl.contents:  # Find all file names in the directory(contents)
            if file.class_name == "Directory":
                dir_name = dir_name + [file.name]
        if name in dir_name:  # It is already exist
            print("The directory already exists!")
            return

        new_dir = Directory(name, [])
        if owner:  # specify the owner.
            new_dir.chown(owner)
        self.cdl.contents = self.cdl.contents + [new_dir]  # add new directory

    def remove_from_list(self, old_list, item):
        new_list = []
        for n in old_list:
            if n != item:
                new_list = new_list + [n]
        return new_list

    #  remove a file from the current working directory
    def rm(self, name):
        for file in self.cdl.contents:
            if file.name == name and file.class_name == "Directory":
                if file.contents == []:  # Directory has to be empty to be removed.
                    self.cdl.contents = self.remove_from_list(self.cdl.contents, file)
                    return
                else:
                    print("Sorry, the directory is not empty")
                return
            if file.name == name and file.class_name == "PlainFile":
                self.cdl.contents = self.remove_from_list(self.cdl.contents, file)
                return

    # find a file name in a file system and returns the path to the first occurrence of the file
    def find_file(self, file_name, cdl):
        for file in cdl.contents:
            if file.class_name == "PlainFile":
                if file.name == file_name:
                    return f"{cdl.name}/{file_name}"
            else:
                route = self.find_file(file_name, file)
                if route:
                    return f"{cdl.name}/{route}"
        return

    def find(self, name):
        cdl = self.find_file(name, self.cdl)
        if cdl == None:  # False if it does not exist.
            return False
        return cdl

    # change the owner of a single file or directory.
    def chown_r(self, owner, cdl=None):
        if not cdl:
            cdl = self.cdl
        cdl.chown(owner)
        if cdl.class_name == "Directory":
            for file in cdl.contents:
                self.chown_r(owner, file)


print("Testing question 1")

# question 1 should allow to create simple files and folders:
file = PlainFile("boot.exe")
folder = Directory("Downloads", [])

root = Directory("root", [PlainFile("boot.exe"),
                          Directory("home", [
                              Directory("thor",
                                        [PlainFile("hunde.jpg"),
                                         PlainFile("quatsch.txt")]),
                              Directory("isaac",
                                        [PlainFile("gatos.jpg")])])])

print("Testing question 2")

# question 2: implement the str

print(root)
"""
Directory(root,[PlainFile(boot.exe),Directory(home,[Directory(thor,[PlainFile(hunde.jpg),PlainFile(quatsch.txt)],Directory(isaac,[PlainFile(gatos.jpg)]]]
"""

print("Testing question 3")

# question 3: test chown()
file = PlainFile("boot.exe")
folder = Directory("Downloads", [])
print(f'file.owner: {file.owner}; folder: {folder.owner}')
file.chown("root")
folder.chown("isaac")
print(f'file.owner: {file.owner}; folder: {folder.owner}')

print("Testing question 4")

# question 4: ls() doesn't return anything but prints.
root.ls()
"""
root
	boot.exe
	home
		thor
			hunde.jpg
			quatsch.txt
		isaac
			gatos.jpg
"""

# question 5: create FileSystem
print("Testing question 5a: basic filesystem and pwd")

fs = FileSystem(root)

# 5a:
print(fs.pwd())

print("Testing question 5b: ls in working directory")

# 5b:
fs.ls()

# 5c:

print("Testing question 5c: cd")

# if you try to move to a non existing directory or to a file,
# the method should complain:
fs.cd("casa")
# But you can move to an existing directory in the working directory.
fs.cd("home")
# if we now do ls(), you should only see the content in home:
fs.ls()

# you can't go backwards yet...

print("Testing question 5d:  mkdir and create file")
fs = FileSystem(root)  # re-initialise fs

fs.mkdir(
    "test")  # the owner of the directory should be 'default' as not indicated.  fs.mkdir("test","isaac") would set the owner to isaac
fs.cd("test")
fs.create_file("test.txt")
fs.ls()

print("Testing question 5e:  dot dot")

# to test this properly, let's create the entire file system using our previous functions!

root = Directory("root", [], owner="root")
fs = FileSystem(root)
fs.create_file(
    "boot.exe")  # when creating a file we do not need to indicate owner, it will be the same as the working directory
fs.mkdir("test")
fs.cd("test")
fs.create_file("test.txt")
fs.cd("..")
fs.mkdir("home", owner="root")
fs.cd("home")
fs.mkdir("thor", owner="thor")
fs.mkdir("isaac", owner="isaac")
fs.cd("thor")
fs.create_file("hunde.jpg")
fs.create_file("quatsch.txt")
fs.cd("..")
fs.cd("isaac")
fs.create_file("gatos.jpg")
fs.cd("..")
fs.cd("..")
fs.ls()

print("Testing question 5f:  rm")

fs.rm("test")  # shouldn't work!
fs.cd("test")
fs.rm("test.txt")
fs.cd("..")
fs.rm("test")
fs.ls()

print("Testing question 5e:  find")

print(fs.find("gatos.jpg"))
fs.cd("home")
print(fs.find("boot.exe"))  # shouldn't find it!

print(fs.find("thor"))  # should print the relative path "home/thor"