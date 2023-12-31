# cmdgpt
#### Execute GPT Queries Directly from the Command Line
The output will pretty print the ChatGPT Markdown answer to console.


cmdgpt offers two modes for querying:

1. **Single Question Mode**: Directly ask a question in the command line like so:

   ```
   cmdgpt "What is the meaning of life?"
   ```

2. **Interactive Session Mode**: Enter a continuous query session by simply typing `cmdgpt`. Within this mode, you can ask multiple questions:

   ```
   cmdgpt
   > What is the meaning of life?
   ...
   ```
3. **Image Generation with Dall-e**: first word should be `pic` or `pix`

   ```
   cmdgpt pic "image of a cat"
   ```

   - Using `pix` will instruct Dall-e not to add any details to your prompt.
   - Images are 1024x1024, HD quality.
