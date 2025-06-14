import { Module } from '@nestjs/common';
import { OpenaiService } from './openai.service';
import OpenAI from 'openai';
import { ConfigModule, ConfigService } from '@nestjs/config';

@Module({
    imports: [ConfigModule],
    providers: [OpenaiService, 
        {
          provide: OpenAI,
          useFactory: (configService: ConfigService) => {
            const apiKey = configService.get<string>("AI_KEY");
            return new OpenAI({apiKey});
          },
          inject: [ConfigService]
        },
      ],
    exports: [OpenaiService]
})
export class OpenaiModule {}
