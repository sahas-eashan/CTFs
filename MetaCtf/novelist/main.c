#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define TITLE_MAX_CHARS 32
#define PAGE_SIZE 4096
#define MAX_BOOKS 5

typedef struct {
    char title[TITLE_MAX_CHARS];
    size_t num_pages;
    char* content;
} book_t;

book_t* books[MAX_BOOKS];

void init() {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

void fatal(const char* msg) {
    puts(msg);
    exit(1);
}

size_t read_n(char* buf, size_t n) {
    char c;
    size_t i = 0;
    while(i < n) {
        if(read(0, &c, 1) != 1) {
            break;
        }

        if(c == '\n') {
            break;
        }

        buf[i++] = c;
    }
    return i;
}

void menu() {
    puts("Write your next hit book with Novelist!");
    puts("1. Start a new book");
    puts("2. Write into a book");
    puts("3. Read a book");
    puts("4. Delete a book");
    puts("5. Exit");
    printf("> ");
}

void start_book() {
    int created = 0;
    for(int i = 0; i < MAX_BOOKS; i++) {
        if(books[i] != NULL) continue;
        created = 1;

        book_t* book = (book_t*) malloc(sizeof(book_t));
        printf("Enter your book's title: ");
        read_n(book->title, TITLE_MAX_CHARS);
        printf("Enter your book's page count: ");
        if(scanf("%lu", &(book->num_pages)) != 1) {
            fatal("Invalid page count");
        }
        book->content = (char*) malloc(book->num_pages * PAGE_SIZE);

        books[i] = book;
        break;
    }

    if(created) {
        puts("Book created!");
    } else {
        puts("No more book slots!");
    }
}

void write_book() {
    int book_idx;

    printf("Enter book index: ");
    if(scanf("%d", &book_idx) != 1 || !(0 <= book_idx < MAX_BOOKS) || books[book_idx] == NULL) {
        puts("Invalid book");
        return;
    }

    book_t* book = books[book_idx];
    for(int i = 0; i < book->num_pages; i++) {
        printf("Page %d: ", i + 1);
        if(read_n(book->content + i * PAGE_SIZE, PAGE_SIZE) == 0) break;
    }
}

void read_book() {
    int book_idx;
    char trunc[256];

    printf("Enter book index: ");
    if(scanf("%d", &book_idx) != 1 || !(0 <= book_idx < MAX_BOOKS) || books[book_idx] == NULL) {
        puts("Invalid book");
        return;
    }
    
    book_t* book = books[book_idx];
    memcpy(trunc, book->content, 256);
    puts(book->title);
    puts(trunc);
}

void delete_book() {
    int book_idx;

    printf("Enter book index: ");
    if(scanf("%d", &book_idx) != 1 || !(0 <= book_idx < MAX_BOOKS) || books[book_idx] == NULL) {
        puts("Invalid book");
        return;
    }
    book_t* book = books[book_idx];
    free(book->content);
    free(book);
    books[book_idx] = NULL;
}

int main () {
    init();

    int choice;

    while(1) {
        menu();
        if(scanf("%d", &choice) != 1) {
            break;
        }
        if(choice == 1) {
            start_book();
        } else if(choice == 2) {
            write_book();
        } else if(choice == 3) {
            read_book();
        } else if(choice == 4) {
            delete_book();
        } else if(choice == 5) {
            break;
        }
    }
}
