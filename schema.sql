create table entity_type
(
    id          char(2) primary key,
    color_code  char(6)     not null,
    name        varchar(30) not null,
    description TEXT
);

insert into entity_type
values ('pe', '1875be', 'Person'),
       ('gr', '5cd755', 'Group'),
       ('to', '894bab', 'Town'),
       ('de', 'aaaaaa', 'Deity'),
       ('ar', 'd441b2', 'Area'),
       ('pl', 'c85252', 'Place'),
       ('pr', 'dedc37', 'Player'),
       ('np', 'fea74f', 'Non-Person')
;

create table entity
(
    id               serial primary key,
    entity_type_code char(2)     not null references entity_type (id),
    first_name       varchar(64) not null,
    last_name        varchar(64),
    unique (first_name, last_name),
    title            varchar(64),
    status           varchar(64),
    active           boolean     not null default true,
    created_at       timestamp   not null default CURRENT_TIMESTAMP,
    updated_at       timestamp   not null default CURRENT_TIMESTAMP
);

create index ix_entity_type on entity (entity_type_code, active);

create table entity_relation
(
    id               serial primary key,
    source_entity_id int         not null references entity (id),
    target_entity_id int         not null references entity (id),
    relation         varchar(64) not null,
    unique (source_entity_id, target_entity_id, relation),
    active           boolean     not null default true,
    mutual           boolean     not null default false,
    created_at       timestamp   not null default CURRENT_TIMESTAMP,
    updated_at       timestamp   not null default CURRENT_TIMESTAMP,
    check (source_entity_id <> target_entity_id)
);

create index ix_relation_source_status on entity_relation (source_entity_id, active);
create index ix_relation_target_status on entity_relation (target_entity_id, active);

CREATE FUNCTION explode_entity_relations(primary_entity_id int) RETURNS SETOF entity_relation AS
$$
WITH RECURSIVE exploded AS (SELECT *
                            FROM entity_relation e
                            WHERE source_entity_id = $1
                              AND active = true
                            UNION ALL
                            SELECT er.*
                            FROM entity_relation er
                                     JOIN exploded e on er.source_entity_id = e.target_entity_id
                            WHERE er.target_entity_id != $1
                              AND er.source_entity_id != e.source_entity_id
                              AND er.active = true)
SELECT *
FROM entity_relation
WHERE id in (SELECT DISTINCT id
             FROM exploded)
$$ LANGUAGE SQL;

insert into entity (entity_type_code, first_name, last_name, title, status)
values ('pe', 'John', 'Doe', 'Mr.', 'Alive'),
       ('pe', 'Jane', 'Doe', 'Mrs.', 'Alive'),
       ('pe', 'John', 'Smith', 'Mr.', 'Alive'),
       ('pe', 'Jane', 'Smith', 'Mrs.', 'Alive'),
       ('pe', 'John', 'Jones', 'Mr.', 'Alive'),
       ('pe', 'Jane', 'Jones', 'Mrs.', 'Alive'),
       ('pe', 'John', 'Brown', 'Mr.', 'Alive'),
       ('pe', 'Jane', 'Brown', 'Mrs.', 'Alive'),
       ('pe', 'John', 'White', 'Mr.', 'Alive'),
       ('pe', 'Jane', 'White', 'Mrs.', 'Alive'),
       ('pe', 'John', 'Black', 'Mr.', 'Alive'),
       ('pe', 'Jane', 'Black', 'Mrs.', 'Alive'),
       ('pe', 'John', 'Green', 'Mr.', 'Alive'),
       ('pe', 'Jane', 'Green', 'Mrs.', 'Alive'),
       ('pe', 'John', 'Blue', 'Mr.', 'Alive'),
       ('pe', 'Jane', 'Blue', 'Mrs.', 'Alive'),
       ('pe', 'John', 'Purple', 'Mr.', 'Alive'),
       ('pe', 'Jane', 'Purple', 'Mrs.', 'Alive'),
       ('pe', 'John', 'Orange', 'Mr.', 'Alive'),
       ('pe', 'Jane', 'Orange', 'Mrs.', 'Alive'),
       ('pe', 'John', 'Yellow', 'Mr.', 'Alive')
;

insert into entity_relation (source_entity_id, target_entity_id, relation, active)
values (1, 2, 'spouse', true),
       (1, 3, 'friend', true),
       (1, 4, 'friend', true),
       (3, 5, 'friend', true),
       (3, 6, 'friend', true),
       (3, 9, 'friend', true),
       (7, 8, 'friend', true),
       (7, 9, 'friend', true),
       (7, 10, 'friend', true),
       (7, 11, 'friend', true),
       (1, 12, 'friend', true),
       (1, 13, 'friend', true),
       (1, 14, 'friend', true),
       (1, 15, 'friend', true),
       (1, 16, 'friend', true),
       (1, 17, 'friend', true),
       (1, 18, 'friend', true)
;
