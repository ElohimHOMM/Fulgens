create table BAN_CHANNEL (
    CHANNEL_ID BIGINT not null,
    GUILD_ID BIGINT not null,
    primary key (CHANNEL_ID, GUILD_ID)
)