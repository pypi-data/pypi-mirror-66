def test_compile_query():
    ids = list(range(1, 4))
    query = file_table.update() \
        .values(id=None) \
        .where(file_table.c.id.in_(ids))
    q, p = connection.compile_query(query)
    assert q == 'UPDATE meows SET id=$1 WHERE meows.id IN ($2, $3, $4)'
    assert p == [None, 1, 2, 3]