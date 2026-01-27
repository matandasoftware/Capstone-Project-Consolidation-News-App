from django.shortcuts import render, get_object_or_404, redirect
from .models import Note
from .forms import NoteForm 


# Create your views here.
def note_list(request):
    """
    Display all notes ordered by creation date (newest first).
    """

    notes = Note.objects.all().order_by('-created_at')
    return render(request, 'notes/note_list.html', {'notes': notes})


def note_detail(request, pk):
    """
    Display a single note by its primary key.
    """

    note_obj = get_object_or_404(Note, pk=pk)
    return render(request, 'notes/note_detail.html', {'note': note_obj})


def note_create(request):
    """
    Create a new note. Displays form on GET, saves note on POST.
    """

    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('note_list')
    else:
        form = NoteForm()
    return render(request, 'notes/note_form.html', {'form': form})


def note_update(request, pk):
    """
    Update an existing note. Pre-fills form with current data.
    """

    note_obj = get_object_or_404(Note, pk=pk)
    if request.method == "POST":
        form = NoteForm(request.POST, instance=note_obj)
        if form.is_valid():
            form.save()
            return redirect('note_detail', pk=note_obj.pk)
    else:
        form = NoteForm(instance=note_obj)
    return render(request, 'notes/note_form.html', {'form': form})


def note_delete(request, pk):
    """
    Delete a note. Shows confirmation page on GET, deletes on POST.
    """

    note_obj = get_object_or_404(Note, pk=pk)
    if request.method == "POST":
        note_obj.delete()
        return redirect('note_list')
    return render(request, 'notes/note_confirm_delete.html', {'note': note_obj})
