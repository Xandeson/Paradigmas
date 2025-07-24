from django.shortcuts import render
from .models import Course
from .models import Student
from django.shortcuts import get_object_or_404, redirect

def dashboard(request):
    """Dashboard principal com estatísticas"""
    courses = Course.objects.all()
    students = Student.objects.all()
    
    # Estatísticas
    total_courses = courses.count()
    total_students = students.count()
    active_students = students.filter(status='active').count()
    graduated_students = students.filter(status='graduated').count()
    
    # Cursos mais populares
    popular_courses = courses.annotate(
        student_count=Count('students')
    ).order_by('-student_count')[:5]
    
    # Últimos alunos cadastrados
    recent_students = students.order_by('-created_at')[:5]
    
    context = {
        'total_courses': total_courses,
        'total_students': total_students,
        'active_students': active_students,
        'graduated_students': graduated_students,
        'popular_courses': popular_courses,
        'recent_students': recent_students,
    }
    
    return render(request, 'dashboard.html', context)
      
def course_list(request):
    """Lista todos os cursos"""
    courses = Course.objects.all()
    return render(request, 'core/course_list.html', {'courses': courses})


def course_create(request):
    """Criar novo curso"""
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Curso criado com sucesso!')
            return redirect('course_list')
    else:
        form = CourseForm()
    
    return render(request, 'course_form.html', {
        'form': form,
        'title': 'Novo Curso'
    })


def course_edit(request, pk):
    """Editar curso existente"""
    course = get_object_or_404(Course, pk=pk)
    
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, 'Curso atualizado com sucesso!')
            return redirect('course_list')
    else:
        form = CourseForm(instance=course)
    
    return render(request, 'course_form.html', {
        'form': form,
        'title': 'Editar Curso',
        'course': course
    })


def course_delete(request, pk):
    """Deletar curso"""
    course = get_object_or_404(Course, pk=pk)
    
    if request.method == 'POST':
        course.delete()
        messages.success(request, 'Curso excluído com sucesso!')
        return redirect('course_list')
    
    return render(request, 'course_confirm_delete.html', {'course': course})


# Views de Alunos
def student_list(request):
    """Lista todos os alunos"""
    students = Student.objects.select_related('course').all()
    return render(request, 'student_list.html', {'students': students})


def student_create(request):
    """Criar novo aluno"""
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Aluno cadastrado com sucesso!')
            return redirect('student_list')
    else:
        form = StudentForm()
    
    return render(request, 'student_form.html', {
        'form': form,
        'title': 'Novo Aluno'
    })


def student_edit(request, pk):
    """Editar aluno existente"""
    student = get_object_or_404(Student, pk=pk)
    
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Aluno atualizado com sucesso!')
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)
    
    return render(request, 'student_form.html', {
        'form': form,
        'title': 'Editar Aluno',
        'student': student
    })


def student_delete(request, pk):
    """Deletar aluno"""
    student = get_object_or_404(Student, pk=pk)
    
    if request.method == 'POST':
        student.delete()
        messages.success(request, 'Aluno excluído com sucesso!')
        return redirect('student_list')
    
    return render(request, 'student_confirm_delete.html', {'student': student})

# Create your views here.
