import { Module } from '@nestjs/common';
import { VeshunService } from './veshun.service';
import { VeshunController } from './veshun.controller';
import { OpenaiModule } from './openai/openai.module';
import { OpenaiService } from './openai/openai.service';
import { ConfigModule, ConfigService } from '@nestjs/config';
import OpenAI from 'openai';

@Module({
  imports: [OpenaiModule, ConfigModule.forRoot()],
  controllers: [VeshunController],
  providers: [VeshunService, OpenaiService,
    {
      provide: OpenAI,
      useFactory: (configService: ConfigService) => {
        const apiKey = configService.get<string>("AI_KEY");
        return new OpenAI({apiKey});
      },
      inject: [ConfigService]
    },
  ],
})
export class VeshunModule {}
