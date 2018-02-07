#include "library.h"

void by_ptr(struct Foo_s *foo) {
    foo->bar += 1;
}