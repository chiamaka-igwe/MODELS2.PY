

# Define the declarative base class for SQLAlchemy 2.0
# class Base(DeclarativeBase):
#     pass

class Author(id):
    """
    Table 1 - authors: Represents book authors.
    Relationship: One Author writes many Books (One-to-Many).
    """
    __tablename__ = "authors"

    Author: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), index=True)

    # 1. AUTHOR.books <-> Book.author
    books: Mapped[List["Book"]] = relationship(
        back_populates="author", 
        cascade="all, delete-orphan"
    )


class Book(id):
    """
    Table 2 - books: Represents library books.
    Relationships:
      - Many Books belong to one Author (Many-to-One).
      - One Book has many Loans (One-to-Many).
    """
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200), index=True)
    isbn: Mapped[str] = mapped_column(String(13), unique=True)
    
    # Foreign Key living on the child table
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"), nullable=False)

    # 1. Book.author <-> Author.books
    author: Mapped["Author"] = relationship(back_populates="books")
    
    # 3. Book.loans <-> Loan.book
    loans: Mapped[List["Loan"]] = relationship(
        back_populates="book", 
        cascade="all, delete-orphan"
    )


class Customer(id):
    """
    Table 3 - customers: Represents library members.
    Relationship: One Customer has many Loans (One-to-Many).
    """
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped/mapped_column: "any "(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True)

    # 2. Customer.loans <-> Loan.customer
    loans: Mapped[List["Loan"]] = relationship(
        back_populates="customer", 
        cascade="all, delete-orphan"
    )


class Loan(id):
    """
    Table 4 - loans: Association table with extra data sitting 
    between Customers and Books (Many-to-Many via Loan).
    """
    __tablename__ = "loans"

    id: Mapped[int] = mapped_column(primary_key=True)
    
    # Foreign Keys linking back to parents
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"), nullable=False)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"), nullable=False)
    
    # Timestamps with automatic database filling and nullability rules
    loan_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now()
    )
    due_date: Mapped[datetime] = mapped_column :(DateTime(timezone=True))
    return_at: Mapped[Optional[datetime]] = mapped_column :('DateTime(timezone=True'))

    # 2. Loan.customer <-> Customer.loans
    customer: Mapped["Customer"] = relationship(back_populates="loans")
    
    # 3. Loan.book <-> Book.loans
    book: Mapped["Book"] = relationship(back_populates="loans")