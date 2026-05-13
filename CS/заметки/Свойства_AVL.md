
AVL-дерево — самобалансирующееся двоичное дерево поиска, в котором для каждого узла **фактор баланса** (разность высот левого и правого поддеревьев) по модулю не превышает $1$:
$$ \text{balance}(v) = \text{height}(v.\text{left}) - \text{height}(v.\text{right}) \in \{-1, 0, 1\} $$

## Гарантированная высота
Из условия баланса следует, что высота AVL-дерева с $n$ узлами не превышает $1.44 \log_2 n$. Поэтому время поиска, вставки и удаления составляет $O(\log n)$ в худшем случае.

## Реализация на Си
Структура узла с явным хранением высоты поддерева:
```c
typedef struct AVLNode {
    int key;
    struct AVLNode *left, *right;
    int height;
} AVLNode;

int get_height(AVLNode *v) {
    return v ? v->height : 0;
}

void update_height(AVLNode *v) {
    int hl = get_height(v->left);
    int hr = get_height(v->right);
    v->height = (hl > hr ? hl : hr) + 1;
}

int balance_factor(AVLNode *v) {
    return get_height(v->left) - get_height(v->right);
}
```

При вставке и удалении баланс может нарушиться; восстановление выполняется серией поворотов (см. [[Балансировка_AVL_после_вставки]], [[Балансировка_AVL_после_удаления]]).

## Связанные заметки
- [[AVL-дерево]]
- [[Балансировка_AVL_после_вставки]], [[Балансировка_AVL_после_удаления]]

---