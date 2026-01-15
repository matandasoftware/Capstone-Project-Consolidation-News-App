
"""
views.py for Sticky Notes app

Defines views for CRUD operations on sticky notes.

Author: [Your Name]
"""

from django.shortcuts import render, get_object_or_404, redirect
from .models import StickyNote
from .forms import StickyNoteForm

def note_list(request):
    """
    Display a list of all sticky notes.
    """


    notes = StickyNote.objects.all()
    return render(request, 'notes/note_list.html', {'notes': notes})

def note_detail(request, pk):
    """
    Display details for a single sticky note.
    """


    note = get_object_or_404(StickyNote, pk=pk)
    return render(request, 'notes/note_detail.html', {'note': note})

def note_create(request):
    """
    Create a new sticky note.
    """


    if request.method == 'POST':
        form = StickyNoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('note_list')
    else:
        form = StickyNoteForm()
    return render(request, 'notes/note_form.html', {'form': form})

def note_update(request, pk):
    """
    Update an existing sticky note.
    """


    note = get_object_or_404(StickyNote, pk=pk)
    if request.method == 'POST':
        form = StickyNoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('note_detail', pk=note.pk)
    else:
        form = StickyNoteForm(instance=note)
    return render(request, 'notes/note_form.html', {'form': form})

def note_delete(request, pk):
    """
    Delete a sticky note.
    """


    note = get_object_or_404(StickyNote, pk=pk)
    if request.method == 'POST':
        note.delete()
        return redirect('note_list')
    return render(request, 'notes/note_confirm_delete.html', {'note': note})
