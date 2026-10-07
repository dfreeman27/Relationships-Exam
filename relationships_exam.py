
from sqlalchemy import (
    create_engine,
    String,
    ForeignKey,
    Table,
    Column,
    Integer
)

from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    Session
)


# ============================================================
# DATABASE
# ============================================================

engine = create_engine("sqlite:///school.db", echo=False)


# ============================================================
# BASE CLASS
# ============================================================

class Base(DeclarativeBase):
    pass


# ============================================================
# MANY-TO-MANY ASSOCIATION TABLE
# Course <-> Student
# ============================================================

student_courses = Table(
    "student_courses",
    Base.metadata,

    Column(
        "student_id",
        Integer,
        ForeignKey("students.id"),
        primary_key=True
    ),

    Column(
        "course_id",
        Integer,
        ForeignKey("courses.id"),
        primary_key=True
    )
)


# ============================================================
# DEPARTMENT
# One Department -> Many Teachers
# ============================================================

class Department(Base):
    __tablename__ = "departments"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    teachers: Mapped[list["Teacher"]] = relationship(
        back_populates="department"
    )

    def __repr__(self):
        return f"Department(name='{self.name}')"


# ============================================================
# TEACHER
# Many Teachers -> One Department
# One Teacher -> Many Courses
# ============================================================

class Teacher(Base):
    __tablename__ = "teachers"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    department_id: Mapped[int] = mapped_column(
        ForeignKey("departments.id")
    )

    department: Mapped["Department"] = relationship(
        back_populates="teachers"
    )

    courses: Mapped[list["Course"]] = relationship(
        back_populates="teacher"
    )

    def __repr__(self):
        return f"Teacher(name='{self.name}')"


# ============================================================
# COURSE
# Many Courses -> One Teacher
# Many Courses <-> Many Students
# ============================================================

class Course(Base):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    teacher_id: Mapped[int] = mapped_column(
        ForeignKey("teachers.id")
    )

    teacher: Mapped["Teacher"] = relationship(
        back_populates="courses"
    )

    students: Mapped[list["Student"]] = relationship(
        secondary=student_courses,
        back_populates="courses"
    )

    def __repr__(self):
        return f"Course(name='{self.name}')"


# ============================================================
# STUDENT
# Many Students <-> Many Courses
# ============================================================

class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    courses: Mapped[list["Course"]] = relationship(
        secondary=student_courses,
        back_populates="students"
    )

    def __repr__(self):
        return f"Student(name='{self.name}')"


# ============================================================
# CREATE TABLES
# ============================================================

Base.metadata.create_all(engine)

print("Tables created!")


# ============================================================
# INSERT SAMPLE DATA
# ============================================================

with Session(engine) as session:

    # --------------------------------------------------------
    # Departments
    # --------------------------------------------------------

    science = Department(name="Science")
    mathematics = Department(name="Mathematics")
    english = Department(name="English")

    # --------------------------------------------------------
    # Teachers
    # --------------------------------------------------------

    alice = Teacher(
        name="Alice Johnson",
        department=science
    )

    bob = Teacher(
        name="Bob Smith",
        department=mathematics
    )

    carol = Teacher(
        name="Carol Williams",
        department=english
    )

    # --------------------------------------------------------
    # Courses
    # --------------------------------------------------------

    biology = Course(
        name="Biology 101",
        teacher=alice
    )

    chemistry = Course(
        name="Chemistry 101",
        teacher=alice
    )

    algebra = Course(
        name="Algebra 101",
        teacher=bob
    )

    calculus = Course(
        name="Calculus 101",
        teacher=bob
    )

    literature = Course(
        name="English Literature",
        teacher=carol
    )

    # --------------------------------------------------------
    # Students
    # --------------------------------------------------------

    student1 = Student(name="John Doe")
    student2 = Student(name="Jane Smith")
    student3 = Student(name="Mike Brown")
    student4 = Student(name="Sarah Davis")
    student5 = Student(name="David Wilson")
    student6 = Student(name="Emily Johnson")

    # --------------------------------------------------------
    # Enroll students in courses
    # --------------------------------------------------------

    biology.students = [
        student1,
        student2,
        student3,
        student4
    ]

    chemistry.students = [
        student1,
        student2,
        student5
    ]

    algebra.students = [
        student2,
        student3,
        student4,
        student5,
        student6
    ]

    calculus.students = [
        student1,
        student3,
        student6
    ]

    literature.students = [
        student4,
        student5
    ]

    # --------------------------------------------------------
    # Add everything
    # --------------------------------------------------------

    session.add_all([
        science,
        mathematics,
        english,
        alice,
        bob,
        carol,
        biology,
        chemistry,
        algebra,
        calculus,
        literature,
        student1,
        student2,
        student3,
        student4,
        student5,
        student6
    ])

    session.commit()

    print("Sample data created!")


# ============================================================
# DEMO QUERIES
# ============================================================

with Session(engine) as session:

    # --------------------------------------------------------
    # 1. Each department and its teachers
    # --------------------------------------------------------

    print("\n" + "=" * 50)
    print("DEPARTMENTS AND THEIR TEACHERS")
    print("=" * 50)

    departments = session.query(Department).all()

    for department in departments:

        print(f"\nDepartment: {department.name}")

        for teacher in department.teachers:
            print(f"  Teacher: {teacher.name}")


    # --------------------------------------------------------
    # 2. Each teacher and the courses they teach
    # --------------------------------------------------------

    print("\n" + "=" * 50)
    print("TEACHERS AND THEIR COURSES")
    print("=" * 50)

    teachers = session.query(Teacher).all()

    for teacher in teachers:

        print(f"\nTeacher: {teacher.name}")
        print(f"Department: {teacher.department.name}")

        for course in teacher.courses:
            print(f"  Course: {course.name}")


    # --------------------------------------------------------
    # 3. Each course with its enrolled students
    # --------------------------------------------------------

    print("\n" + "=" * 50)
    print("COURSES AND ENROLLED STUDENTS")
    print("=" * 50)

    courses = session.query(Course).all()

    for course in courses:

        print(f"\nCourse: {course.name}")
        print(f"Teacher: {course.teacher.name}")

        for student in course.students:
            print(f"  Student: {student.name}")


    # --------------------------------------------------------
    # 4. Each student and the courses they're enrolled in
    # --------------------------------------------------------

    print("\n" + "=" * 50)
    print("STUDENTS AND THEIR COURSES")
    print("=" * 50)

    students = session.query(Student).all()

    for student in students:

        print(f"\nStudent: {student.name}")

        for course in student.courses:
            print(f"  Course: {course.name}")


    # --------------------------------------------------------
    # 5. Any course with more than 3 students
    # --------------------------------------------------------

    print("\n" + "=" * 50)
    print("COURSES WITH MORE THAN 3 STUDENTS")
    print("=" * 50)

    for course in courses:

        if len(course.students) > 3:
            print(
                f"{course.name}: "
                f"{len(course.students)} students"
            )
