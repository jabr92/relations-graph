create table entity_type
(
    id          char(2) primary key,
    color_code  char(6)     not null,
    name        varchar(50) not null,
    description varchar(255)
);

insert into entity_type
values ('pe', '1875be', 'person'),
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
    id         serial primary key,
    entity_type       char(2)     not null references entity_type (id),
    first_name varchar(64) not null,
    last_name  varchar(64),
    title      varchar(64),
    status     varchar(64)
);

create table entity_relation
(
    entity_id        int         not null references entity (id),
    target_entity_id int         not null references entity (id),
    relation_type    varchar(64) not null,
    primary key (entity_id, target_entity_id, relation_type),
    mutual           boolean     not null default false,
    active           boolean     not null default true,
    created_at       timestamp   not null default CURRENT_TIMESTAMP,
    updated_at       timestamp
);
