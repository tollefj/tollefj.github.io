require 'json'

module Jekyll
  class ExampleJsonGenerator < Generator
    safe true
    priority :low

    def generate(site)
      posts_data = []
      site.posts.docs.each do |post|
        puts "Processing post: #{post.data['title']}"
        post_info = {
          'title' => post.data['title'],
          'tags' => post.data['tags'] || [],
          'description' => post.data['description'] || "",
          'url' => post.url,
        }
        posts_data << post_info
      end

      # Create the example data structure
      example_data = {
        'generated_at' => Time.now.strftime('%Y-%m-%d %H:%M:%S'),
        'total_posts' => site.posts.docs.length,
        'sample_posts' => posts_data,
        'site_info' => {
          'title' => site.config['title'],
          'description' => site.config['description']
        }
      }

      outfile = File.join(site.source, 'assets', 'searchData.json')

      # Write the data to EXAMPLE.json
      File.open(outfile, 'w') do |file| 
        file.write(JSON.pretty_generate(example_data))
      end
      
      # Let Jekyll know about the new file
      site.static_files << Jekyll::StaticFile.new(site, site.source, 'assets', 'searchData.json') do |file|
        file.write(JSON.pretty_generate(example_data))
      end
    end
  end
end