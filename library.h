#include <stdint.h>

typedef struct Foo_s {
    uint16_t bar;
} Foo;

void by_ptr(Foo *foo);
