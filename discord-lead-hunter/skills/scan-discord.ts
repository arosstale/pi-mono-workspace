import { DiscordClient, GatewayIntentBits } from 'discord.js';

export interface LeadCandidate {
  discordHandle: string;
  userId: number | string;
  content: string;
  serverName: string;
  channelName: string;
  timestamp: string;
}

export interface SearchConfig {
  servers: string[];
  channels: string[];
  keywords: string[];
  limit: number;
}

/**
 * Scrape Discord servers/channels looking for users asking for help/agency/dev
 * Returns: array of LeadCandidate
 */
export async function scanDiscordChannels(config: SearchConfig): Promise<LeadCandidate[]> {
  const client = new DiscordClient({
    intents: [
      GatewayIntentBits.Guilds,
      GatewayIntentBits.GuildMessages,
      GatewayIntentBits.MessageContent
    ]
  });

  await client.login(process.env.DISCORD_TOKEN!);
  
  const leads: LeadCandidate[] = [];

  for (const serverId of config.servers) {
    try {
      const server = await client.guilds.fetch(serverId);
      
      for (const channel of server.channels.cache.values()) {
        if (!channel.isTextBased() || !config.channels.includes(channel.name)) {
          continue;
        }

        // Fetch recent messages (last 100)
        const messages = await channel.messages.fetch({ limit: 100 });
        
        for (const [_, msg] of messages) {
          const text = msg.content.toLowerCase();
          
          // Check if message matches our criteria
          const matchesKeywords = config.keywords.some(
            keyword => text.includes(keyword.toLowerCase())
          );
          
          if (!matchesKeywords) continue;
          
          // Extract lead info
          leads.push({
            discordHandle: msg.author.tag,
            userId: msg.author.id,
            content: msg.content,
            serverName: server.name,
            channelName: channel.name,
            timestamp: new Date(msg.createdTimestamp).toISOString()
          });
        }
      }
    } catch (error) {
      console.error(`Error scanning server ${serverId}:`, error);
    }
  }

  await client.destroy();
  
  // Return top N leads
  return leads.slice(0, config.limit);
}