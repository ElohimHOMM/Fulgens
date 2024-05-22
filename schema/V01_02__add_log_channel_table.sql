create table LOG_CHANNEL (
    CHANNEL_ID BIGINT not null,
    GUILD_ID BIGINT not null,
    primary key (GUILD_ID)
)