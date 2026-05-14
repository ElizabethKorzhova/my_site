"""Module containing model definitions for session application."""
from django.db import models


class Author(models.Model):
    """Model definition for Author.

            Fields:
                name (CharField): required."""
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        """String representation of Author model."""
        return self.name


class BookData(models.Model):
    """Model definition for BookData.

            Fields:
                title (CharField): required;
                author (ForeignKey): required;
                published_year (PositiveIntegerField): optional."""
    title = models.CharField(max_length=150, db_index=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")
    published_year = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        """Metaclass for BookData model."""
        indexes = [models.Index(fields=["title"])]

    def __str__(self) -> str:
        """String representation of Book model."""
        return self.title


class Review(models.Model):
    """Model definition for Review.

            Fields:
                book (ForeignKey): required;
                text (CharField): required;
                rating (PositiveIntegerField): required."""
    book = models.ForeignKey(BookData, on_delete=models.CASCADE, related_name="reviews")
    text = models.TextField()
    rating = models.PositiveSmallIntegerField(db_index=True)

    class Meta:
        """Metaclass for Review model."""
        indexes = [
            models.Index(fields=["rating"]),
            models.Index(fields=["book", "rating"]),
        ]

    def __str__(self) -> str:
        """String representation of Review model."""
        return f"{self.book.title} - {self.rating}"
