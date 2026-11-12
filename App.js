import React, { useState } from "react";
import {
  SafeAreaView,
  View,
  Text,
  TextInput,
  ScrollView,
  Pressable,
  StyleSheet,
  StatusBar,
  Alert,
} from "react-native";

// --------------------------------------------------
// TOKENTRAIL - MOCK DATA
// --------------------------------------------------

const articles = [
  {
    id: 1,
    category: "AI Research",
    title: "OpenAI introduces new advances in AI reasoning",
    description:
      "Researchers are working on AI systems that can solve complex problems through improved reasoning and planning.",
    source: "AI Research",
    date: "Today",
    readTime: "4 min read",
    tag: "Research",
    content:
      "Modern AI reasoning systems aim to solve multi-step problems more reliably. These developments focus on planning, logical thinking, and evaluating possible solutions before producing an answer.",
  },
  {
    id: 2,
    category: "Generative AI",
    title: "The future of generative AI is becoming more multimodal",
    description:
      "AI models are increasingly learning to understand text, images, audio and video together.",
    source: "Technology Update",
    date: "Yesterday",
    readTime: "5 min read",
    tag: "Generative AI",
    content:
      "Multimodal AI combines different types of information. Instead of understanding only text, these systems can work with images, audio, video, and other forms of data to provide richer experiences.",
  },
  {
    id: 3,
    category: "AI Tools",
    title: "AI coding assistants are changing software development",
    description:
      "Developers are using AI tools to understand code, generate suggestions and improve productivity.",
    source: "Developer World",
    date: "2 days ago",
    readTime: "3 min read",
    tag: "Development",
    content:
      "AI coding assistants can help developers understand unfamiliar code, identify errors, write tests, and explore solutions. They support developers but do not replace the need to understand programming fundamentals.",
  },
  {
    id: 4,
    category: "Machine Learning",
    title: "Smaller AI models are gaining attention",
    description:
      "Efficient AI models can make intelligent features more accessible on everyday devices.",
    source: "ML Today",
    date: "3 days ago",
    readTime: "4 min read",
    tag: "Machine Learning",
    content:
      "Smaller models aim to reduce computational requirements while remaining useful for specific tasks. This can make AI applications faster, more affordable, and easier to run locally.",
  },
  {
    id: 5,
    category: "AI Research",
    title: "Open-source AI research continues to grow",
    description:
      "Developers and researchers are sharing models, datasets and tools with the global community.",
    source: "Research Hub",
    date: "4 days ago",
    readTime: "3 min read",
    tag: "Open Source",
    content:
      "Open-source AI encourages collaboration. Developers can inspect available code, experiment with models, contribute improvements, and learn from research shared by the community.",
  },
];

const snippets = [
  {
    id: 1,
    category: "AI Basics",
    title: "What is Artificial Intelligence?",
    short:
      "Artificial Intelligence enables machines to perform tasks that normally require human intelligence.",
    full:
      "Artificial Intelligence is a field of computer science focused on building systems that can perform tasks such as learning, reasoning, problem-solving, understanding language, and recognizing patterns. Examples include virtual assistants, recommendation systems, and smart search.",
    level: "Beginner",
    time: "2 min",
  },
  {
    id: 2,
    category: "Machine Learning",
    title: "What is Machine Learning?",
    short:
      "Machine Learning allows computers to learn patterns from data instead of following only fixed instructions.",
    full:
      "Machine Learning is a subset of AI. A model learns from examples and uses the patterns it discovers to make predictions or decisions. Common types include supervised learning, unsupervised learning, and reinforcement learning.",
    level: "Beginner",
    time: "3 min",
  },
  {
    id: 3,
    category: "Deep Learning",
    title: "Understanding Neural Networks",
    short:
      "Neural networks are computing systems inspired by the way biological neurons process information.",
    full:
      "A neural network consists of connected nodes arranged in layers. Each connection has a weight. During training, the network adjusts these weights to reduce prediction errors. Neural networks are widely used in image recognition, speech processing, and language tasks.",
    level: "Intermediate",
    time: "4 min",
  },
  {
    id: 4,
    category: "Generative AI",
    title: "What is Generative AI?",
    short:
      "Generative AI creates new content such as text, images, audio, video and code.",
    full:
      "Generative AI systems learn patterns from training data and use those patterns to generate new outputs. Large language models and image-generation systems are common examples.",
    level: "Beginner",
    time: "3 min",
  },
  {
    id: 5,
    category: "LLMs",
    title: "What are Large Language Models?",
    short:
      "LLMs are AI models trained on large amounts of text to understand and generate language.",
    full:
      "Large Language Models use neural network architectures, commonly transformers, to process and generate text. They can assist with writing, summarization, coding, question answering, and many other language tasks.",
    level: "Intermediate",
    time: "4 min",
  },
  {
    id: 6,
    category: "AI Basics",
    title: "What are AI Hallucinations?",
    short:
      "An AI hallucination happens when an AI system generates information that sounds convincing but is incorrect.",
    full:
      "AI models generate responses based on learned patterns. Sometimes they produce inaccurate facts, invented references, or unsupported answers. Important information should always be checked against reliable sources.",
    level: "Beginner",
    time: "2 min",
  },
];

const exploreResources = [
  {
    id: 1,
    title: "ChatGPT",
    category: "AI Tools",
    type: "AI Assistant",
    description:
      "An AI assistant for learning, writing, coding, brainstorming and problem-solving.",
    tags: ["AI", "Productivity", "Learning"],
    link: "https://chatgpt.com",
  },
  {
    id: 2,
    title: "Google Gemini",
    category: "AI Tools",
    type: "AI Model",
    description:
      "Google's AI model family designed for reasoning and working across different types of information.",
    tags: ["LLM", "Multimodal", "AI"],
    link: "https://gemini.google.com",
  },
  {
    id: 3,
    title: "Cursor",
    category: "Development",
    type: "AI Code Editor",
    description:
      "An AI-powered code editor that helps developers understand and work with code.",
    tags: ["Coding", "Developer", "IDE"],
    link: "https://cursor.com",
  },
  {
    id: 4,
    title: "Perplexity",
    category: "AI Tools",
    type: "AI Search",
    description:
      "An AI-powered search and answer platform that helps explore information with sources.",
    tags: ["Search", "Research", "AI"],
    link: "https://www.perplexity.ai",
  },
  {
    id: 5,
    title: "LangChain",
    category: "Frameworks",
    type: "AI Framework",
    description:
      "A framework for building applications powered by language models.",
    tags: ["LLM", "Framework", "Development"],
    link: "https://www.langchain.com",
  },
  {
    id: 6,
    title: "TensorFlow",
    category: "Frameworks",
    type: "ML Framework",
    description:
      "An open-source platform used to build and train machine learning models.",
    tags: ["Machine Learning", "Python", "Framework"],
    link: "https://www.tensorflow.org",
  },
  {
    id: 7,
    title: "Hugging Face Transformers",
    category: "Repositories",
    type: "Open-source Library",
    description:
      "A popular library providing access to pretrained models for NLP, vision and audio tasks.",
    tags: ["Models", "Open Source", "NLP"],
    link: "https://huggingface.co",
  },
  {
    id: 8,
    title: "Attention Is All You Need",
    category: "Research",
    type: "Research Paper",
    description:
      "The research paper that introduced the Transformer architecture.",
    tags: ["Research", "Transformers", "Deep Learning"],
    link: "https://arxiv.org/abs/1706.03762",
  },
];

const headlineCategories = [
  "All",
  "AI Research",
  "Generative AI",
  "AI Tools",
  "Machine Learning",
];

const snippetCategories = [
  "All",
  "AI Basics",
  "Machine Learning",
  "Deep Learning",
  "Generative AI",
  "LLMs",
];

const resourceCategories = [
  "All",
  "AI Tools",
  "Development",
  "Frameworks",
  "Repositories",
  "Research",
];

// --------------------------------------------------
// MAIN APP
// --------------------------------------------------

export default function App() {
  const [user, setUser] = useState(null);
  const [authScreen, setAuthScreen] = useState("login");

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [fullName, setFullName] = useState("");

  const [activeTab, setActiveTab] = useState("Home");
  const [selectedArticle, setSelectedArticle] = useState(null);

  const [savedArticles, setSavedArticles] = useState([]);
  const [readSnippets, setReadSnippets] = useState([]);
  const [expandedSnippet, setExpandedSnippet] = useState(null);
  const [expandedResource, setExpandedResource] = useState(null);
  const [exploredResources, setExploredResources] = useState([]);

  const [headlineSearch, setHeadlineSearch] = useState("");
  const [snippetSearch, setSnippetSearch] = useState("");
  const [resourceSearch, setResourceSearch] = useState("");

  const [headlineCategory, setHeadlineCategory] = useState("All");
  const [snippetCategory, setSnippetCategory] = useState("All");
  const [resourceCategory, setResourceCategory] = useState("All");

  // ------------------------------------------------
  // AUTHENTICATION - FRONTEND DEMO
  // ------------------------------------------------

  const handleLogin = () => {
    if (!email.trim() || !password.trim()) {
      Alert.alert("Missing details", "Please enter your email and password.");
      return;
    }

    if (!email.includes("@") || password.length < 6) {
      Alert.alert(
        "Invalid details",
        "Enter a valid email and a password of at least 6 characters."
      );
      return;
    }

    setUser({
      name: email.split("@")[0],
      email: email.trim(),
    });

    setActiveTab("Home");
  };

  const handleSignup = () => {
    if (!fullName.trim() || !email.trim() || !password.trim()) {
      Alert.alert("Missing details", "Please fill in all the fields.");
      return;
    }

    if (!email.includes("@")) {
      Alert.alert("Invalid email", "Please enter a valid email address.");
      return;
    }

    if (password.length < 6) {
      Alert.alert(
        "Weak password",
        "Your password must contain at least 6 characters."
      );
      return;
    }

    setUser({
      name: fullName.trim(),
      email: email.trim(),
    });

    setActiveTab("Home");
  };

  const handleLogout = () => {
    Alert.alert("Log out", "Are you sure you want to log out?", [
      { text: "Cancel", style: "cancel" },
      {
        text: "Log out",
        style: "destructive",
        onPress: () => {
          setUser(null);
          setPassword("");
          setEmail("");
          setFullName("");
          setAuthScreen("login");
          setSelectedArticle(null);
        },
      },
    ]);
  };

  // ------------------------------------------------
  // CONTENT ACTIONS
  // ------------------------------------------------

  const toggleBookmark = (id) => {
    setSavedArticles((previous) =>
      previous.includes(id)
        ? previous.filter((item) => item !== id)
        : [...previous, id]
    );
  };

  const markSnippetRead = (id) => {
    setReadSnippets((previous) =>
      previous.includes(id) ? previous : [...previous, id]
    );
  };

  const markResourceExplored = (id) => {
    setExploredResources((previous) =>
      previous.includes(id) ? previous : [...previous, id]
    );
  };

  // ------------------------------------------------
  // FILTERED CONTENT
  // ------------------------------------------------

  const filteredArticles = articles.filter((article) => {
    const matchesCategory =
      headlineCategory === "All" ||
      article.category === headlineCategory;

    const matchesSearch =
      article.title.toLowerCase().includes(headlineSearch.toLowerCase()) ||
      article.description.toLowerCase().includes(headlineSearch.toLowerCase());

    return matchesCategory && matchesSearch;
  });

  const filteredSnippets = snippets.filter((snippet) => {
    const matchesCategory =
      snippetCategory === "All" ||
      snippet.category === snippetCategory;

    const matchesSearch =
      snippet.title.toLowerCase().includes(snippetSearch.toLowerCase()) ||
      snippet.short.toLowerCase().includes(snippetSearch.toLowerCase());

    return matchesCategory && matchesSearch;
  });

  const filteredResources = exploreResources.filter((resource) => {
    const matchesCategory =
      resourceCategory === "All" ||
      resource.category === resourceCategory;

    const matchesSearch =
      resource.title.toLowerCase().includes(resourceSearch.toLowerCase()) ||
      resource.description.toLowerCase().includes(resourceSearch.toLowerCase());

    return matchesCategory && matchesSearch;
  });

  const progressPercentage = Math.round(
    ((readSnippets.length + exploredResources.length) /
      (snippets.length + exploreResources.length)) *
      100
  );

  // ------------------------------------------------
  // REUSABLE COMPONENTS
  // ------------------------------------------------

  const Header = ({ title, subtitle, showLogout = true }) => (
    <View style={styles.header}>
      <View style={{ flex: 1 }}>
        <Text style={styles.brandSmall}>TOKENTRAIL</Text>
        <Text style={styles.headerTitle}>{title}</Text>
        {subtitle ? <Text style={styles.headerSubtitle}>{subtitle}</Text> : null}
      </View>

      {showLogout && user ? (
        <Pressable style={styles.profileButton} onPress={handleLogout}>
          <Text style={styles.profileInitial}>
            {user.name.charAt(0).toUpperCase()}
          </Text>
        </Pressable>
      ) : null}
    </View>
  );

  const SectionHeading = ({ title, action, onPress }) => (
    <View style={styles.sectionHeading}>
      <Text style={styles.sectionTitle}>{title}</Text>
      {action ? (
        <Pressable onPress={onPress}>
          <Text style={styles.sectionAction}>{action}</Text>
        </Pressable>
      ) : null}
    </View>
  );

  const SearchBar = ({ value, onChangeText, placeholder }) => (
    <View style={styles.searchBox}>
      <Text style={styles.searchIcon}>⌕</Text>
      <TextInput
        style={styles.searchInput}
        placeholder={placeholder}
        placeholderTextColor="#8B96AA"
        value={value}
        onChangeText={onChangeText}
      />
      {value.length > 0 ? (
        <Pressable onPress={() => onChangeText("")}>
          <Text style={styles.clearSearch}>×</Text>
        </Pressable>
      ) : null}
    </View>
  );

  const CategoryList = ({ items, selected, onSelect }) => (
    <ScrollView
      horizontal
      showsHorizontalScrollIndicator={false}
      contentContainerStyle={styles.categoryList}
    >
      {items.map((item) => (
        <Pressable
          key={item}
          onPress={() => onSelect(item)}
          style={[
            styles.categoryChip,
            selected === item && styles.categoryChipActive,
          ]}
        >
          <Text
            style={[
              styles.categoryText,
              selected === item && styles.categoryTextActive,
            ]}
          >
            {item}
          </Text>
        </Pressable>
      ))}
    </ScrollView>
  );

  const EmptyState = ({ title, message }) => (
    <View style={styles.emptyState}>
      <Text style={styles.emptyIcon}>✦</Text>
      <Text style={styles.emptyTitle}>{title}</Text>
      <Text style={styles.emptyMessage}>{message}</Text>
    </View>
  );

  // ------------------------------------------------
  // HOME SCREEN
  // ------------------------------------------------

  const renderHome = () => (
    <ScrollView
      showsVerticalScrollIndicator={false}
      contentContainerStyle={styles.screenContent}
    >
      <Header
        title={`Hello, ${user?.name || "Explorer"} 👋`}
        subtitle="Your personal AI learning space"
      />

      <View style={styles.heroCard}>
        <View style={styles.heroShine} />
        <Text style={styles.heroEyebrow}>YOUR AI JOURNEY STARTS HERE</Text>
        <Text style={styles.heroTitle}>
          Stay curious.{"\n"}Keep exploring.
        </Text>
        <Text style={styles.heroDescription}>
          Discover what's happening in AI, understand new concepts and track
          your learning journey.
        </Text>

        <Pressable
          style={styles.heroButton}
          onPress={() => setActiveTab("Headlines")}
        >
          <Text style={styles.heroButtonText}>Explore AI Updates  →</Text>
        </Pressable>

        <View style={styles.heroDecoration}>
          <Text style={styles.heroDecorationText}>AI</Text>
        </View>
      </View>

      <View style={styles.statsRow}>
        <View style={styles.statCard}>
          <Text style={styles.statIcon}>▤</Text>
          <Text style={styles.statNumber}>{articles.length}</Text>
          <Text style={styles.statLabel}>Headlines</Text>
        </View>

        <View style={styles.statCard}>
          <Text style={styles.statIcon}>✧</Text>
          <Text style={styles.statNumber}>{readSnippets.length}</Text>
          <Text style={styles.statLabel}>Learned</Text>
        </View>

        <View style={styles.statCard}>
          <Text style={styles.statIcon}>◈</Text>
          <Text style={styles.statNumber}>{exploredResources.length}</Text>
          <Text style={styles.statLabel}>Explored</Text>
        </View>
      </View>

      <SectionHeading
        title="Your learning progress"
        action="View all"
        onPress={() => setActiveTab("Progress")}
      />

      <View style={styles.progressCard}>
        <View style={styles.progressTop}>
          <View>
            <Text style={styles.cardHeading}>AI Explorer Journey</Text>
            <Text style={styles.mutedText}>Keep moving forward!</Text>
          </View>
          <Text style={styles.progressPercent}>{progressPercentage}%</Text>
        </View>

        <View style={styles.progressTrack}>
          <View
            style={[styles.progressFill, { width: `${progressPercentage}%` }]}
          />
        </View>

        <Text style={styles.progressFootnote}>
          {readSnippets.length + exploredResources.length} of{" "}
          {snippets.length + exploreResources.length} learning activities
          completed
        </Text>
      </View>

      <SectionHeading
        title="Latest AI headlines"
        action="See all"
        onPress={() => setActiveTab("Headlines")}
      />

      {articles.slice(0, 3).map((article) => (
        <Pressable
          key={article.id}
          style={styles.articleCard}
          onPress={() => setSelectedArticle(article)}
        >
          <View style={styles.cardTopLine}>
            <Text style={styles.tag}>{article.category}</Text>
            <Text style={styles.cardDate}>{article.date}</Text>
          </View>

          <Text style={styles.articleTitle}>{article.title}</Text>
          <Text style={styles.articleDescription} numberOfLines={2}>
            {article.description}
          </Text>

          <Text style={styles.readMore}>Read story →</Text>
        </Pressable>
      ))}

      <SectionHeading
        title="Start learning"
        action="View all"
        onPress={() => setActiveTab("Snippets")}
      />

      <View style={styles.quickLearnCard}>
        <View style={styles.quickLearnIcon}>
          <Text style={styles.quickLearnIconText}>✦</Text>
        </View>
        <View style={{ flex: 1 }}>
          <Text style={styles.cardHeading}>Learn AI in small steps</Text>
          <Text style={styles.mutedText}>
            Short explanations that make complex concepts easier.
          </Text>
        </View>
        <Pressable
          style={styles.roundArrow}
          onPress={() => setActiveTab("Snippets")}
        >
          <Text style={styles.roundArrowText}>→</Text>
        </Pressable>
      </View>
    </ScrollView>
  );

  // ------------------------------------------------
  // HEADLINES SCREEN
  // ------------------------------------------------

  const renderHeadlines = () => (
    <ScrollView
      showsVerticalScrollIndicator={false}
      contentContainerStyle={styles.screenContent}
    >
      <Header
        title="AI Headlines"
        subtitle="Stay informed about what's happening in AI"
      />

      <SearchBar
        value={headlineSearch}
        onChangeText={setHeadlineSearch}
        placeholder="Search AI headlines..."
      />

      <CategoryList
        items={headlineCategories}
        selected={headlineCategory}
        onSelect={setHeadlineCategory}
      />

      <View style={styles.resultCount}>
        <Text style={styles.mutedText}>
          {filteredArticles.length} updates found
        </Text>
        <Text style={styles.blueSmall}>LATEST UPDATES</Text>
      </View>

      {filteredArticles.length === 0 ? (
        <EmptyState
          title="No headlines found"
          message="Try another search or category."
        />
      ) : (
        filteredArticles.map((article) => (
          <View key={article.id} style={styles.articleCard}>
            <View style={styles.cardTopLine}>
              <Text style={styles.tag}>{article.category}</Text>
              <Pressable onPress={() => toggleBookmark(article.id)}>
                <Text style={styles.bookmarkIcon}>
                  {savedArticles.includes(article.id) ? "♥" : "♡"}
                </Text>
              </Pressable>
            </View>

            <Text style={styles.articleTitle}>{article.title}</Text>
            <Text style={styles.articleDescription}>
              {article.description}
            </Text>

            <View style={styles.articleFooter}>
              <Text style={styles.cardDate}>
                {article.source}  ·  {article.readTime}
              </Text>
              <Pressable onPress={() => setSelectedArticle(article)}>
                <Text style={styles.readMore}>Read more →</Text>
              </Pressable>
            </View>
          </View>
        ))
      )}

      <SectionHeading title="Your saved headlines" />

      {savedArticles.length === 0 ? (
        <Text style={styles.savedHint}>
          Tap the heart on a headline to save it here.
        </Text>
      ) : (
        articles
          .filter((article) => savedArticles.includes(article.id))
          .map((article) => (
            <Pressable
              key={article.id}
              style={styles.savedCard}
              onPress={() => setSelectedArticle(article)}
            >
              <Text style={styles.savedTitle}>{article.title}</Text>
              <Text style={styles.blueSmall}>SAVED STORY  →</Text>
            </Pressable>
          ))
      )}
    </ScrollView>
  );

  // ------------------------------------------------
  // SNIPPETS SCREEN
  // ------------------------------------------------

  const renderSnippets = () => (
    <ScrollView
      showsVerticalScrollIndicator={false}
      contentContainerStyle={styles.screenContent}
    >
      <Header
        title="AI Snippets"
        subtitle="Understand AI, one concept at a time"
      />

      <View style={styles.snippetIntro}>
        <Text style={styles.snippetIntroTitle}>Small lessons. Big ideas.</Text>
        <Text style={styles.snippetIntroText}>
          Explore simple explanations of important AI concepts.
        </Text>
        <Text style={styles.snippetIntroCount}>
          {readSnippets.length} / {snippets.length} completed
        </Text>
      </View>

      <SearchBar
        value={snippetSearch}
        onChangeText={setSnippetSearch}
        placeholder="Search concepts..."
      />

      <CategoryList
        items={snippetCategories}
        selected={snippetCategory}
        onSelect={setSnippetCategory}
      />

      {filteredSnippets.length === 0 ? (
        <EmptyState
          title="No concepts found"
          message="Try searching for another AI concept."
        />
      ) : (
        filteredSnippets.map((snippet, index) => {
          const isExpanded = expandedSnippet === snippet.id;
          const isRead = readSnippets.includes(snippet.id);

          return (
            <View key={snippet.id} style={styles.snippetCard}>
              <View style={styles.snippetCardTop}>
                <View style={styles.snippetNumber}>
                  <Text style={styles.snippetNumberText}>
                    {String(index + 1).padStart(2, "0")}
                  </Text>
                </View>
                <View style={{ flex: 1 }}>
                  <Text style={styles.tag}>{snippet.category}</Text>
                  <Text style={styles.snippetTitle}>{snippet.title}</Text>
                </View>
                {isRead ? <Text style={styles.completedMark}>✓</Text> : null}
              </View>

              <Text style={styles.snippetShort}>{snippet.short}</Text>

              {isExpanded ? (
                <View style={styles.expandedContent}>
                  <Text style={styles.expandedText}>{snippet.full}</Text>
                  <Text style={styles.levelText}>
                    {snippet.level}  ·  {snippet.time}
                  </Text>
                </View>
              ) : null}

              <View style={styles.snippetFooter}>
                <Pressable
                  onPress={() => {
                    setExpandedSnippet(isExpanded ? null : snippet.id);
                    if (!isRead) markSnippetRead(snippet.id);
                  }}
                >
                  <Text style={styles.readMore}>
                    {isExpanded ? "Show less ↑" : "Read explanation →"}
                  </Text>
                </Pressable>

                <Text style={styles.cardDate}>{snippet.time}</Text>
              </View>
            </View>
          );
        })
      )}
    </ScrollView>
  );

  // ------------------------------------------------
  // PROGRESS SCREEN
  // ------------------------------------------------

  const renderProgress = () => (
    <ScrollView
      showsVerticalScrollIndicator={false}
      contentContainerStyle={styles.screenContent}
    >
      <Header
        title="My Progress"
        subtitle="Every small step counts"
      />

      <View style={styles.progressHero}>
        <View style={styles.progressHeroShine} />
        <Text style={styles.progressHeroLabel}>YOUR OVERALL PROGRESS</Text>
        <Text style={styles.progressHeroNumber}>{progressPercentage}%</Text>
        <Text style={styles.progressHeroText}>
          You're building your AI knowledge journey.
        </Text>

        <View style={styles.progressTrackLight}>
          <View
            style={[
              styles.progressFillLight,
              { width: `${progressPercentage}%` },
            ]}
          />
        </View>
      </View>

      <SectionHeading title="Learning statistics" />

      <View style={styles.progressStatsGrid}>
        <View style={styles.progressStatCard}>
          <Text style={styles.progressStatIcon}>✧</Text>
          <Text style={styles.progressStatNumber}>
            {readSnippets.length}
          </Text>
          <Text style={styles.progressStatLabel}>Snippets read</Text>
          <Text style={styles.progressStatSub}>of {snippets.length}</Text>
        </View>

        <View style={styles.progressStatCard}>
          <Text style={styles.progressStatIcon}>◈</Text>
          <Text style={styles.progressStatNumber}>
            {exploredResources.length}
          </Text>
          <Text style={styles.progressStatLabel}>Resources explored</Text>
          <Text style={styles.progressStatSub}>
            of {exploreResources.length}
          </Text>
        </View>

        <View style={styles.progressStatCard}>
          <Text style={styles.progressStatIcon}>♥</Text>
          <Text style={styles.progressStatNumber}>
            {savedArticles.length}
          </Text>
          <Text style={styles.progressStatLabel}>Saved headlines</Text>
          <Text style={styles.progressStatSub}>Your collection</Text>
        </View>

        <View style={styles.progressStatCard}>
          <Text style={styles.progressStatIcon}>▤</Text>
          <Text style={styles.progressStatNumber}>
            {articles.length}
          </Text>
          <Text style={styles.progressStatLabel}>Available updates</Text>
          <Text style={styles.progressStatSub}>AI headlines</Text>
        </View>
      </View>

      <SectionHeading title="Your achievements" />

      <View style={styles.achievementCard}>
        <View style={styles.achievementIcon}>
          <Text style={styles.achievementEmoji}>🌱</Text>
        </View>
        <View style={{ flex: 1 }}>
          <Text style={styles.cardHeading}>First Steps</Text>
          <Text style={styles.mutedText}>
            Complete your first AI learning activity.
          </Text>
        </View>
        <Text style={styles.achievementStatus}>
          {readSnippets.length + exploredResources.length > 0
            ? "Unlocked ✓"
            : "Locked"}
        </Text>
      </View>

      <View style={styles.achievementCard}>
        <View style={styles.achievementIcon}>
          <Text style={styles.achievementEmoji}>📚</Text>
        </View>
        <View style={{ flex: 1 }}>
          <Text style={styles.cardHeading}>Knowledge Seeker</Text>
          <Text style={styles.mutedText}>
            Read at least 3 AI snippets.
          </Text>
        </View>
        <Text style={styles.achievementStatus}>
          {readSnippets.length >= 3 ? "Unlocked ✓" : "Locked"}
        </Text>
      </View>

      <View style={styles.achievementCard}>
        <View style={styles.achievementIcon}>
          <Text style={styles.achievementEmoji}>🚀</Text>
        </View>
        <View style={{ flex: 1 }}>
          <Text style={styles.cardHeading}>AI Explorer</Text>
          <Text style={styles.mutedText}>
            Explore at least 3 AI resources.
          </Text>
        </View>
        <Text style={styles.achievementStatus}>
          {exploredResources.length >= 3 ? "Unlocked ✓" : "Locked"}
        </Text>
      </View>

      <View style={styles.encouragementCard}>
        <Text style={styles.encouragementTitle}>Keep the momentum going!</Text>
        <Text style={styles.encouragementText}>
          Explore one new concept or resource today. Your progress grows with
          every activity.
        </Text>
        <Pressable
          style={styles.encouragementButton}
          onPress={() => setActiveTab("Snippets")}
        >
          <Text style={styles.encouragementButtonText}>Continue learning →</Text>
        </Pressable>
      </View>
    </ScrollView>
  );

  // ------------------------------------------------
  // EXPLORE AI SCREEN
  // ------------------------------------------------

  const renderExplore = () => (
    <ScrollView
      showsVerticalScrollIndicator={false}
      contentContainerStyle={styles.screenContent}
    >
      <Header
        title="Explore AI"
        subtitle="Discover tools, models, frameworks and research"
      />

      <View style={styles.exploreHero}>
        <Text style={styles.exploreHeroEyebrow}>DISCOVER WHAT'S NEXT</Text>
        <Text style={styles.exploreHeroTitle}>
          Find your next AI discovery.
        </Text>
        <Text style={styles.exploreHeroDescription}>
          Explore useful technologies and resources from across the AI
          ecosystem.
        </Text>
      </View>

      <SearchBar
        value={resourceSearch}
        onChangeText={setResourceSearch}
        placeholder="Search tools, models, research..."
      />

      <CategoryList
        items={resourceCategories}
        selected={resourceCategory}
        onSelect={setResourceCategory}
      />

      <View style={styles.resultCount}>
        <Text style={styles.mutedText}>
          {filteredResources.length} resources available
        </Text>
        <Text style={styles.blueSmall}>
          {exploredResources.length} EXPLORED
        </Text>
      </View>

      {filteredResources.length === 0 ? (
        <EmptyState
          title="No resources found"
          message="Try another keyword or category."
        />
      ) : (
        filteredResources.map((resource, index) => {
          const isExpanded = expandedResource === resource.id;
          const isExplored = exploredResources.includes(resource.id);

          return (
            <View key={resource.id} style={styles.resourceCard}>
              <View style={styles.resourceTop}>
                <View style={styles.resourceIcon}>
                  <Text style={styles.resourceIconText}>
                    {["✦", "◈", "</>", "⌕", "⚙", "▦", "⬡", "✧"][index % 8]}
                  </Text>
                </View>

                <View style={{ flex: 1 }}>
                  <Text style={styles.resourceType}>{resource.type}</Text>
                  <Text style={styles.resourceTitle}>{resource.title}</Text>
                </View>

                {isExplored ? (
                  <Text style={styles.completedMark}>✓</Text>
                ) : null}
              </View>

              <Text style={styles.resourceDescription}>
                {resource.description}
              </Text>

              <View style={styles.tagRow}>
                {resource.tags.map((tag) => (
                  <Text key={tag} style={styles.resourceTag}>
                    {tag}
                  </Text>
                ))}
              </View>

              {isExpanded ? (
                <View style={styles.resourceExtra}>
                  <Text style={styles.mutedText}>
                    Category: {resource.category}
                  </Text>
                  <Text style={styles.resourceUrl}>{resource.link}</Text>
                </View>
              ) : null}

              <View style={styles.resourceFooter}>
                <Pressable
                  onPress={() => {
                    setExpandedResource(isExpanded ? null : resource.id);
                    if (!isExplored) markResourceExplored(resource.id);
                  }}
                >
                  <Text style={styles.readMore}>
                    {isExpanded ? "Show less ↑" : "Explore details →"}
                  </Text>
                </Pressable>

                <Text style={styles.cardDate}>
                  {isExplored ? "Explored" : "Not explored"}
                </Text>
              </View>
            </View>
          );
        })
      )}
    </ScrollView>
  );

  // ------------------------------------------------
  // ARTICLE DETAIL SCREEN
  // ------------------------------------------------

  const renderArticleDetail = () => {
    if (!selectedArticle) return null;

    const isSaved = savedArticles.includes(selectedArticle.id);

    return (
      <SafeAreaView style={styles.container}>
        <View style={styles.detailHeader}>
          <Pressable
            style={styles.backButton}
            onPress={() => setSelectedArticle(null)}
          >
            <Text style={styles.backButtonText}>←</Text>
          </Pressable>
          <Text style={styles.detailHeaderTitle}>HEADLINE DETAILS</Text>
          <Pressable onPress={() => toggleBookmark(selectedArticle.id)}>
            <Text style={styles.bookmarkIcon}>
              {isSaved ? "♥" : "♡"}
            </Text>
          </Pressable>
        </View>

        <ScrollView contentContainerStyle={styles.detailContent}>
          <Text style={styles.tag}>{selectedArticle.category}</Text>

          <Text style={styles.detailTitle}>{selectedArticle.title}</Text>

          <Text style={styles.detailMeta}>
            {selectedArticle.source}  ·  {selectedArticle.date}  ·  {selectedArticle.readTime}
          </Text>

          <View style={styles.detailDivider} />

          <Text style={styles.detailDescription}>
            {selectedArticle.description}
          </Text>

          <Text style={styles.detailBody}>{selectedArticle.content}</Text>

          <View style={styles.detailNote}>
            <Text style={styles.detailNoteTitle}>TOKENTRAIL INSIGHT</Text>
            <Text style={styles.detailNoteText}>
              Keep exploring AI developments and build your understanding one
              topic at a time.
            </Text>
          </View>

          <Pressable
            style={styles.primaryButton}
            onPress={() => toggleBookmark(selectedArticle.id)}
          >
            <Text style={styles.primaryButtonText}>
              {isSaved ? "Remove from saved" : "Save this headline"}
            </Text>
          </Pressable>
        </ScrollView>
      </SafeAreaView>
    );
  };

  // ------------------------------------------------
  // LOGIN / SIGNUP SCREEN
  // ------------------------------------------------

  const renderAuth = () => (
    <SafeAreaView style={styles.authContainer}>
      <StatusBar barStyle="dark-content" backgroundColor="#F5F8FF" />

      <ScrollView
        contentContainerStyle={styles.authContent}
        keyboardShouldPersistTaps="handled"
      >
        <View style={styles.authLogo}>
          <View style={styles.logoShine} />
          <Text style={styles.authLogoText}>T</Text>
        </View>

        <Text style={styles.authBrand}>TOKENTRAIL</Text>
        <Text style={styles.authHeading}>
          {authScreen === "login"
            ? "Welcome back!"
            : "Create your account"}
        </Text>

        <Text style={styles.authSubtitle}>
          {authScreen === "login"
            ? "Continue your journey into the world of AI."
            : "Start discovering, learning and exploring AI."}
        </Text>

        <View style={styles.authForm}>
          {authScreen === "signup" ? (
            <>
              <Text style={styles.inputLabel}>Full name</Text>
              <TextInput
                style={styles.authInput}
                placeholder="Enter your name"
                placeholderTextColor="#9AA5B8"
                value={fullName}
                onChangeText={setFullName}
                autoCapitalize="words"
              />
            </>
          ) : null}

          <Text style={styles.inputLabel}>Email address</Text>
          <TextInput
            style={styles.authInput}
            placeholder="you@example.com"
            placeholderTextColor="#9AA5B8"
            value={email}
            onChangeText={setEmail}
            keyboardType="email-address"
            autoCapitalize="none"
          />

          <Text style={styles.inputLabel}>Password</Text>
          <TextInput
            style={styles.authInput}
            placeholder="Enter your password"
            placeholderTextColor="#9AA5B8"
            value={password}
            onChangeText={setPassword}
            secureTextEntry
          />

          <Pressable
            style={styles.authPrimaryButton}
            onPress={authScreen === "login" ? handleLogin : handleSignup}
          >
            <View style={styles.authButtonShine} />
            <Text style={styles.authPrimaryButtonText}>
              {authScreen === "login" ? "Log in  →" : "Create account  →"}
            </Text>
          </Pressable>

          <View style={styles.authSwitchRow}>
            <Text style={styles.authSwitchText}>
              {authScreen === "login"
                ? "Don't have an account?"
                : "Already have an account?"}
            </Text>

            <Pressable
              onPress={() =>
                setAuthScreen(authScreen === "login" ? "signup" : "login")
              }
            >
              <Text style={styles.authSwitchLink}>
                {authScreen === "login" ? " Sign up" : " Log in"}
              </Text>
            </Pressable>
          </View>
        </View>

        <Text style={styles.authFooter}>
          DISCOVER  ·  UNDERSTAND  ·  EXPLORE  ·  PROGRESS
        </Text>
      </ScrollView>
    </SafeAreaView>
  );

  // ------------------------------------------------
  // BOTTOM NAVIGATION
  // ------------------------------------------------

  const tabs = [
    { name: "Home", icon: "⌂" },
    { name: "Headlines", icon: "▤" },
    { name: "Snippets", icon: "✧" },
    { name: "Progress", icon: "◔" },
    { name: "Explore", icon: "◈" },
  ];

  const renderBottomNavigation = () => (
    <View style={styles.bottomNav}>
      {tabs.map((tab) => {
        const isActive = activeTab === tab.name;

        return (
          <Pressable
            key={tab.name}
            style={styles.navItem}
            onPress={() => setActiveTab(tab.name)}
          >
            <View
              style={[
                styles.navIconWrap,
                isActive && styles.navIconWrapActive,
              ]}
            >
              <Text
                style={[
                  styles.navIcon,
                  isActive && styles.navIconActive,
                ]}
              >
                {tab.icon}
              </Text>
            </View>

            <Text
              style={[
                styles.navLabel,
                isActive && styles.navLabelActive,
              ]}
            >
              {tab.name}
            </Text>
          </Pressable>
        );
      })}
    </View>
  );

  // ------------------------------------------------
  // APP DISPLAY
  // ------------------------------------------------

  if (!user) {
    return renderAuth();
  }

  if (selectedArticle) {
    return renderArticleDetail();
  }

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="dark-content" backgroundColor="#F5F8FF" />

      <View style={styles.mainContent}>
        {activeTab === "Home" && renderHome()}
        {activeTab === "Headlines" && renderHeadlines()}
        {activeTab === "Snippets" && renderSnippets()}
        {activeTab === "Progress" && renderProgress()}
        {activeTab === "Explore" && renderExplore()}
      </View>

      {renderBottomNavigation()}
    </SafeAreaView>
  );
}

// --------------------------------------------------
// PREMIUM ROYAL BLUE STYLES
// --------------------------------------------------

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#F5F8FF",
  },

  mainContent: {
    flex: 1,
  },

  screenContent: {
    paddingHorizontal: 20,
    paddingTop: 12,
    paddingBottom: 28,
  },

  // HEADER

  header: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    marginBottom: 22,
  },

  brandSmall: {
    color: "#2457E6",
    fontSize: 10,
    fontWeight: "900",
    letterSpacing: 2.5,
    marginBottom: 5,
  },

  headerTitle: {
    color: "#101C3A",
    fontSize: 27,
    fontWeight: "800",
    letterSpacing: -0.8,
  },

  headerSubtitle: {
    color: "#7A879E",
    fontSize: 13,
    marginTop: 5,
    lineHeight: 19,
  },

  profileButton: {
    width: 43,
    height: 43,
    borderRadius: 15,
    backgroundColor: "#2457E6",
    alignItems: "center",
    justifyContent: "center",
    shadowColor: "#2457E6",
    shadowOpacity: 0.24,
    shadowRadius: 10,
    shadowOffset: { width: 0, height: 5 },
    elevation: 5,
  },

  profileInitial: {
    color: "#FFFFFF",
    fontSize: 17,
    fontWeight: "800",
  },

  // HERO

  heroCard: {
    backgroundColor: "#2457E6",
    borderRadius: 27,
    padding: 23,
    minHeight: 255,
    overflow: "hidden",
    marginBottom: 20,
    shadowColor: "#2457E6",
    shadowOpacity: 0.28,
    shadowRadius: 17,
    shadowOffset: { width: 0, height: 9 },
    elevation: 8,
  },

  heroShine: {
    position: "absolute",
    top: -65,
    right: -35,
    width: 190,
    height: 150,
    borderRadius: 100,
    backgroundColor: "rgba(255,255,255,0.13)",
    transform: [{ rotate: "-25deg" }],
  },

  heroEyebrow: {
    color: "#DCE7FF",
    fontSize: 10,
    fontWeight: "800",
    letterSpacing: 1.7,
    marginBottom: 13,
  },

  heroTitle: {
    color: "#FFFFFF",
    fontSize: 32,
    lineHeight: 38,
    fontWeight: "900",
    letterSpacing: -0.7,
  },

  heroDescription: {
    color: "#E3EAFF",
    fontSize: 13,
    lineHeight: 20,
    marginTop: 10,
    maxWidth: "83%",
  },

  heroButton: {
    backgroundColor: "#FFFFFF",
    paddingHorizontal: 17,
    paddingVertical: 12,
    borderRadius: 13,
    alignSelf: "flex-start",
    marginTop: 18,
  },

  heroButtonText: {
    color: "#2457E6",
    fontSize: 12,
    fontWeight: "800",
  },

  heroDecoration: {
    position: "absolute",
    right: -7,
    bottom: 15,
    width: 105,
    height: 105,
    borderRadius: 30,
    borderWidth: 1,
    borderColor: "rgba(255,255,255,0.18)",
    backgroundColor: "rgba(255,255,255,0.09)",
    alignItems: "center",
    justifyContent: "center",
    transform: [{ rotate: "14deg" }],
  },

  heroDecorationText: {
    color: "rgba(255,255,255,0.32)",
    fontSize: 42,
    fontWeight: "900",
  },

  // STATS

  statsRow: {
    flexDirection: "row",
    gap: 10,
    marginBottom: 27,
  },

  statCard: {
    flex: 1,
    backgroundColor: "#FFFFFF",
    paddingVertical: 15,
    paddingHorizontal: 9,
    borderRadius: 18,
    borderWidth: 1,
    borderColor: "#E9EEFA",
  },

  statIcon: {
    color: "#3970F0",
    fontSize: 19,
    marginBottom: 8,
  },

  statNumber: {
    color: "#101C3A",
    fontSize: 23,
    fontWeight: "900",
  },

  statLabel: {
    color: "#8792A7",
    fontSize: 10,
    marginTop: 4,
    fontWeight: "600",
  },

  // SECTION HEADINGS

  sectionHeading: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    marginTop: 7,
    marginBottom: 13,
  },

  sectionTitle: {
    color: "#101C3A",
    fontSize: 18,
    fontWeight: "800",
    letterSpacing: -0.4,
  },

  sectionAction: {
    color: "#2457E6",
    fontSize: 12,
    fontWeight: "800",
  },

  // CARDS

  progressCard: {
    backgroundColor: "#FFFFFF",
    borderRadius: 20,
    padding: 18,
    marginBottom: 26,
    borderWidth: 1,
    borderColor: "#E9EEFA",
  },

  progressTop: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: 15,
  },

  cardHeading: {
    color: "#172441",
    fontSize: 14,
    fontWeight: "800",
  },

  mutedText: {
    color: "#8792A7",
    fontSize: 12,
    lineHeight: 18,
    marginTop: 4,
  },

  progressPercent: {
    color: "#2457E6",
    fontSize: 22,
    fontWeight: "900",
  },

  progressTrack: {
    height: 9,
    backgroundColor: "#E9EFFF",
    borderRadius: 20,
    overflow: "hidden",
  },

  progressFill: {
    height: "100%",
    backgroundColor: "#3970F0",
    borderRadius: 20,
  },

  progressFootnote: {
    color: "#8792A7",
    fontSize: 10,
    marginTop: 10,
  },

  articleCard: {
    backgroundColor: "#FFFFFF",
    padding: 18,
    borderRadius: 20,
    borderWidth: 1,
    borderColor: "#E9EEFA",
    marginBottom: 13,
  },

  cardTopLine: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: 12,
  },

  tag: {
    color: "#2457E6",
    backgroundColor: "#EAF0FF",
    paddingHorizontal: 10,
    paddingVertical: 6,
    borderRadius: 8,
    fontSize: 10,
    fontWeight: "800",
    alignSelf: "flex-start",
    overflow: "hidden",
  },

  cardDate: {
    color: "#929DB0",
    fontSize: 10,
    fontWeight: "600",
  },

  articleTitle: {
    color: "#15213D",
    fontSize: 16,
    lineHeight: 23,
    fontWeight: "800",
    marginBottom: 7,
  },

  articleDescription: {
    color: "#78859B",
    fontSize: 12,
    lineHeight: 19,
  },

  articleFooter: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    marginTop: 16,
  },

  readMore: {
    color: "#2457E6",
    fontSize: 12,
    fontWeight: "800",
  },

  bookmarkIcon: {
    color: "#2457E6",
    fontSize: 23,
    paddingHorizontal: 3,
  },

  quickLearnCard: {
    backgroundColor: "#FFFFFF",
    borderRadius: 19,
    padding: 15,
    flexDirection: "row",
    alignItems: "center",
    gap: 12,
    borderWidth: 1,
    borderColor: "#E9EEFA",
  },

  quickLearnIcon: {
    width: 46,
    height: 46,
    backgroundColor: "#EAF0FF",
    borderRadius: 15,
    alignItems: "center",
    justifyContent: "center",
  },

  quickLearnIconText: {
    color: "#2457E6",
    fontSize: 25,
    fontWeight: "800",
  },

  roundArrow: {
    width: 33,
    height: 33,
    backgroundColor: "#2457E6",
    borderRadius: 12,
    alignItems: "center",
    justifyContent: "center",
  },

  roundArrowText: {
    color: "#FFFFFF",
    fontSize: 19,
    fontWeight: "800",
  },

  // SEARCH

  searchBox: {
    height: 49,
    backgroundColor: "#FFFFFF",
    borderRadius: 15,
    paddingHorizontal: 14,
    flexDirection: "row",
    alignItems: "center",
    borderWidth: 1,
    borderColor: "#E5EBF7",
    marginBottom: 14,
  },

  searchIcon: {
    color: "#2457E6",
    fontSize: 25,
    marginRight: 9,
  },

  searchInput: {
    flex: 1,
    color: "#172441",
    fontSize: 13,
    paddingVertical: 0,
  },

  clearSearch: {
    color: "#7B879B",
    fontSize: 22,
    paddingHorizontal: 5,
  },

  // CATEGORIES

  categoryList: {
    gap: 8,
    paddingBottom: 17,
  },

  categoryChip: {
    backgroundColor: "#FFFFFF",
    borderColor: "#E5EBF7",
    borderWidth: 1,
    paddingHorizontal: 14,
    paddingVertical: 9,
    borderRadius: 12,
  },

  categoryChipActive: {
    backgroundColor: "#2457E6",
    borderColor: "#2457E6",
    shadowColor: "#2457E6",
    shadowOpacity: 0.19,
    shadowRadius: 7,
    shadowOffset: { width: 0, height: 3 },
    elevation: 3,
  },

  categoryText: {
    color: "#758198",
    fontSize: 11,
    fontWeight: "700",
  },

  categoryTextActive: {
    color: "#FFFFFF",
  },

  resultCount: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    marginBottom: 13,
  },

  blueSmall: {
    color: "#3970F0",
    fontSize: 9,
    fontWeight: "900",
    letterSpacing: 1,
  },

  savedHint: {
    color: "#8792A7",
    fontSize: 12,
    marginBottom: 20,
  },

  savedCard: {
    backgroundColor: "#FFFFFF",
    borderRadius: 15,
    padding: 15,
    marginBottom: 10,
    borderWidth: 1,
    borderColor: "#E9EEFA",
  },

  savedTitle: {
    color: "#172441",
    fontSize: 13,
    fontWeight: "700",
    marginBottom: 8,
  },

  // SNIPPETS

  snippetIntro: {
    backgroundColor: "#EAF0FF",
    borderRadius: 20,
    padding: 19,
    marginBottom: 17,
    borderWidth: 1,
    borderColor: "#DCE6FF",
  },

  snippetIntroTitle: {
    color: "#173B9C",
    fontSize: 18,
    fontWeight: "900",
  },

  snippetIntroText: {
    color: "#65799F",
    fontSize: 12,
    lineHeight: 19,
    marginTop: 6,
  },

  snippetIntroCount: {
    color: "#2457E6",
    fontSize: 11,
    fontWeight: "800",
    marginTop: 12,
  },

  snippetCard: {
    backgroundColor: "#FFFFFF",
    borderRadius: 20,
    padding: 17,
    marginBottom: 13,
    borderWidth: 1,
    borderColor: "#E9EEFA",
  },

  snippetCardTop: {
    flexDirection: "row",
    alignItems: "center",
    gap: 12,
  },

  snippetNumber: {
    width: 40,
    height: 40,
    borderRadius: 13,
    backgroundColor: "#EAF0FF",
    alignItems: "center",
    justifyContent: "center",
  },

  snippetNumberText: {
    color: "#2457E6",
    fontSize: 13,
    fontWeight: "900",
  },

  snippetTitle: {
    color: "#172441",
    fontSize: 15,
    fontWeight: "800",
    marginTop: 7,
    flexShrink: 1,
  },

  completedMark: {
    color: "#16865A",
    fontSize: 18,
    fontWeight: "900",
  },

  snippetShort: {
    color: "#77849B",
    fontSize: 12,
    lineHeight: 20,
    marginTop: 14,
  },

  expandedContent: {
    backgroundColor: "#F5F8FF",
    borderRadius: 13,
    padding: 13,
    marginTop: 13,
  },

  expandedText: {
    color: "#53627D",
    fontSize: 12,
    lineHeight: 21,
  },

  levelText: {
    color: "#2457E6",
    fontSize: 10,
    fontWeight: "800",
    marginTop: 10,
  },

  snippetFooter: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    marginTop: 16,
  },

  // PROGRESS

  progressHero: {
    backgroundColor: "#2457E6",
    borderRadius: 25,
    padding: 23,
    overflow: "hidden",
    marginBottom: 25,
    shadowColor: "#2457E6",
    shadowOpacity: 0.25,
    shadowRadius: 14,
    shadowOffset: { width: 0, height: 7 },
    elevation: 6,
  },

  progressHeroShine: {
    position: "absolute",
    right: -50,
    top: -70,
    width: 180,
    height: 150,
    borderRadius: 100,
    backgroundColor: "rgba(255,255,255,0.13)",
  },

  progressHeroLabel: {
    color: "#DCE7FF",
    fontSize: 10,
    fontWeight: "900",
    letterSpacing: 1.5,
  },

  progressHeroNumber: {
    color: "#FFFFFF",
    fontSize: 52,
    fontWeight: "900",
    marginTop: 9,
  },

  progressHeroText: {
    color: "#E2E9FF",
    fontSize: 12,
    marginBottom: 20,
  },

  progressTrackLight: {
    height: 9,
    backgroundColor: "rgba(255,255,255,0.25)",
    borderRadius: 20,
    overflow: "hidden",
  },

  progressFillLight: {
    height: "100%",
    backgroundColor: "#FFFFFF",
    borderRadius: 20,
  },

  progressStatsGrid: {
    flexDirection: "row",
    flexWrap: "wrap",
    gap: 12,
    marginBottom: 25,
  },

  progressStatCard: {
    width: "48%",
    flexGrow: 1,
    backgroundColor: "#FFFFFF",
    borderRadius: 18,
    padding: 17,
    borderWidth: 1,
    borderColor: "#E9EEFA",
  },

  progressStatIcon: {
    color: "#3970F0",
    fontSize: 20,
  },

  progressStatNumber: {
    color: "#172441",
    fontSize: 27,
    fontWeight: "900",
    marginTop: 9,
  },

  progressStatLabel: {
    color: "#52617C",
    fontSize: 11,
    fontWeight: "700",
    marginTop: 3,
  },

  progressStatSub: {
    color: "#9AA5B8",
    fontSize: 10,
    marginTop: 4,
  },

  achievementCard: {
    backgroundColor: "#FFFFFF",
    borderRadius: 17,
    padding: 14,
    flexDirection: "row",
    alignItems: "center",
    gap: 12,
    marginBottom: 10,
    borderWidth: 1,
    borderColor: "#E9EEFA",
  },

  achievementIcon: {
    width: 43,
    height: 43,
    backgroundColor: "#EAF0FF",
    borderRadius: 14,
    alignItems: "center",
    justifyContent: "center",
  },

  achievementEmoji: {
    fontSize: 20,
  },

  achievementStatus: {
    color: "#2457E6",
    fontSize: 10,
    fontWeight: "800",
  },

  encouragementCard: {
    backgroundColor: "#EAF0FF",
    borderRadius: 20,
    padding: 19,
    marginTop: 13,
  },

  encouragementTitle: {
    color: "#173B9C",
    fontSize: 17,
    fontWeight: "900",
  },

  encouragementText: {
    color: "#63769B",
    fontSize: 12,
    lineHeight: 20,
    marginTop: 7,
  },

  encouragementButton: {
    alignSelf: "flex-start",
    backgroundColor: "#2457E6",
    paddingHorizontal: 15,
    paddingVertical: 11,
    borderRadius: 12,
    marginTop: 15,
  },

  encouragementButtonText: {
    color: "#FFFFFF",
    fontSize: 11,
    fontWeight: "800",
  },

  // EXPLORE

  exploreHero: {
    backgroundColor: "#EAF0FF",
    borderRadius: 20,
    padding: 19,
    marginBottom: 17,
    borderWidth: 1,
    borderColor: "#DCE6FF",
  },

  exploreHeroEyebrow: {
    color: "#3970F0",
    fontSize: 9,
    fontWeight: "900",
    letterSpacing: 1.6,
  },

  exploreHeroTitle: {
    color: "#173B9C",
    fontSize: 22,
    lineHeight: 29,
    fontWeight: "900",
    marginTop: 9,
  },

  exploreHeroDescription: {
    color: "#65799F",
    fontSize: 12,
    lineHeight: 19,
    marginTop: 7,
  },

  resourceCard: {
    backgroundColor: "#FFFFFF",
    borderRadius: 20,
    padding: 17,
    borderWidth: 1,
    borderColor: "#E9EEFA",
    marginBottom: 13,
  },

  resourceTop: {
    flexDirection: "row",
    alignItems: "center",
    gap: 12,
  },

  resourceIcon: {
    width: 45,
    height: 45,
    backgroundColor: "#EAF0FF",
    borderRadius: 14,
    alignItems: "center",
    justifyContent: "center",
  },

  resourceIconText: {
    color: "#2457E6",
    fontSize: 20,
    fontWeight: "900",
  },

  resourceType: {
    color: "#8B96AA",
    fontSize: 10,
    fontWeight: "700",
  },

  resourceTitle: {
    color: "#172441",
    fontSize: 15,
    fontWeight: "900",
    marginTop: 4,
  },

  resourceDescription: {
    color: "#77849B",
    fontSize: 12,
    lineHeight: 20,
    marginTop: 13,
  },

  tagRow: {
    flexDirection: "row",
    flexWrap: "wrap",
    gap: 7,
    marginTop: 12,
  },

  resourceTag: {
    color: "#61718E",
    backgroundColor: "#F1F5FC",
    paddingHorizontal: 9,
    paddingVertical: 6,
    borderRadius: 8,
    fontSize: 9,
    fontWeight: "700",
    overflow: "hidden",
  },

  resourceExtra: {
    backgroundColor: "#F5F8FF",
    padding: 12,
    borderRadius: 12,
    marginTop: 13,
  },

  resourceUrl: {
    color: "#2457E6",
    fontSize: 10,
    marginTop: 6,
  },

  resourceFooter: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    marginTop: 16,
  },

  // EMPTY STATE

  emptyState: {
    backgroundColor: "#FFFFFF",
    borderRadius: 20,
    padding: 25,
    alignItems: "center",
    marginVertical: 15,
    borderWidth: 1,
    borderColor: "#E9EEFA",
  },

  emptyIcon: {
    color: "#3970F0",
    fontSize: 30,
    marginBottom: 10,
  },

  emptyTitle: {
    color: "#172441",
    fontSize: 16,
    fontWeight: "800",
  },

  emptyMessage: {
    color: "#8792A7",
    fontSize: 12,
    textAlign: "center",
    marginTop: 6,
    lineHeight: 18,
  },

  // BOTTOM NAVIGATION

  bottomNav: {
    flexDirection: "row",
    backgroundColor: "#FFFFFF",
    paddingTop: 10,
    paddingBottom: 8,
    borderTopWidth: 1,
    borderTopColor: "#E9EEFA",
    justifyContent: "space-around",
  },

  navItem: {
    flex: 1,
    alignItems: "center",
    justifyContent: "center",
    gap: 4,
  },

  navIconWrap: {
    minWidth: 43,
    height: 32,
    borderRadius: 11,
    alignItems: "center",
    justifyContent: "center",
  },

  navIconWrapActive: {
    backgroundColor: "#EAF0FF",
  },

  navIcon: {
    color: "#99A4B8",
    fontSize: 20,
    fontWeight: "700",
  },

  navIconActive: {
    color: "#2457E6",
  },

  navLabel: {
    color: "#929DB0",
    fontSize: 9,
    fontWeight: "700",
  },

  navLabelActive: {
    color: "#2457E6",
    fontWeight: "900",
  },

  // ARTICLE DETAIL

  detailHeader: {
    paddingHorizontal: 20,
    paddingVertical: 13,
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    borderBottomWidth: 1,
    borderBottomColor: "#E9EEFA",
  },

  backButton: {
    width: 38,
    height: 38,
    borderRadius: 12,
    backgroundColor: "#EAF0FF",
    alignItems: "center",
    justifyContent: "center",
  },

  backButtonText: {
    color: "#2457E6",
    fontSize: 22,
    fontWeight: "700",
  },

  detailHeaderTitle: {
    color: "#6E7B92",
    fontSize: 10,
    fontWeight: "900",
    letterSpacing: 1.5,
  },

  detailContent: {
    padding: 22,
    paddingBottom: 40,
  },

  detailTitle: {
    color: "#101C3A",
    fontSize: 27,
    lineHeight: 35,
    fontWeight: "900",
    marginTop: 17,
    letterSpacing: -0.7,
  },

  detailMeta: {
    color: "#8995A9",
    fontSize: 11,
    marginTop: 12,
  },

  detailDivider: {
    height: 1,
    backgroundColor: "#E5EBF7",
    marginVertical: 23,
  },

  detailDescription: {
    color: "#263653",
    fontSize: 16,
    lineHeight: 25,
    fontWeight: "700",
  },

  detailBody: {
    color: "#64728B",
    fontSize: 14,
    lineHeight: 25,
    marginTop: 17,
  },

  detailNote: {
    backgroundColor: "#EAF0FF",
    borderRadius: 17,
    padding: 17,
    marginTop: 25,
  },

  detailNoteTitle: {
    color: "#2457E6",
    fontSize: 10,
    fontWeight: "900",
    letterSpacing: 1.2,
  },

  detailNoteText: {
    color: "#64769A",
    fontSize: 12,
    lineHeight: 20,
    marginTop: 7,
  },

  primaryButton: {
    backgroundColor: "#2457E6",
    borderRadius: 14,
    padding: 16,
    alignItems: "center",
    marginTop: 23,
    shadowColor: "#2457E6",
    shadowOpacity: 0.2,
    shadowRadius: 9,
    shadowOffset: { width: 0, height: 4 },
    elevation: 4,
  },

  primaryButtonText: {
    color: "#FFFFFF",
    fontSize: 13,
    fontWeight: "900",
  },

  // AUTH

  authContainer: {
    flex: 1,
    backgroundColor: "#F5F8FF",
  },

  authContent: {
    flexGrow: 1,
    justifyContent: "center",
    paddingHorizontal: 27,
    paddingVertical: 35,
  },

  authLogo: {
    width: 67,
    height: 67,
    borderRadius: 22,
    backgroundColor: "#2457E6",
    alignItems: "center",
    justifyContent: "center",
    alignSelf: "center",
    marginBottom: 13,
    overflow: "hidden",
    shadowColor: "#2457E6",
    shadowOpacity: 0.3,
    shadowRadius: 13,
    shadowOffset: { width: 0, height: 6 },
    elevation: 7,
  },

  logoShine: {
    position: "absolute",
    top: -19,
    right: -10,
    width: 65,
    height: 40,
    borderRadius: 30,
    backgroundColor: "rgba(255,255,255,0.25)",
    transform: [{ rotate: "-25deg" }],
  },

  authLogoText: {
    color: "#FFFFFF",
    fontSize: 35,
    fontWeight: "900",
  },

  authBrand: {
    color: "#2457E6",
    fontSize: 11,
    fontWeight: "900",
    letterSpacing: 3,
    textAlign: "center",
    marginBottom: 32,
  },

  authHeading: {
    color: "#101C3A",
    fontSize: 29,
    fontWeight: "900",
    textAlign: "center",
    letterSpacing: -0.7,
  },

  authSubtitle: {
    color: "#8792A7",
    fontSize: 13,
    textAlign: "center",
    lineHeight: 20,
    marginTop: 9,
    marginBottom: 29,
  },

  authForm: {
    backgroundColor: "#FFFFFF",
    borderRadius: 24,
    padding: 21,
    borderWidth: 1,
    borderColor: "#E7ECF7",
    shadowColor: "#183A8B",
    shadowOpacity: 0.06,
    shadowRadius: 15,
    shadowOffset: { width: 0, height: 6 },
    elevation: 3,
  },

  inputLabel: {
    color: "#263653",
    fontSize: 12,
    fontWeight: "800",
    marginBottom: 8,
    marginTop: 12,
  },

  authInput: {
    height: 49,
    borderRadius: 13,
    backgroundColor: "#F6F8FC",
    borderWidth: 1,
    borderColor: "#E7ECF7",
    paddingHorizontal: 14,
    color: "#172441",
    fontSize: 13,
  },

  authPrimaryButton: {
    height: 52,
    backgroundColor: "#2457E6",
    borderRadius: 14,
    alignItems: "center",
    justifyContent: "center",
    marginTop: 25,
    overflow: "hidden",
    shadowColor: "#2457E6",
    shadowOpacity: 0.25,
    shadowRadius: 10,
    shadowOffset: { width: 0, height: 5 },
    elevation: 5,
  },

  authButtonShine: {
    position: "absolute",
    top: -18,
    right: 15,
    width: 110,
    height: 35,
    borderRadius: 30,
    backgroundColor: "rgba(255,255,255,0.16)",
    transform: [{ rotate: "-15deg" }],
  },

  authPrimaryButtonText: {
    color: "#FFFFFF",
    fontSize: 14,
    fontWeight: "900",
  },

  authSwitchRow: {
    flexDirection: "row",
    justifyContent: "center",
    alignItems: "center",
    marginTop: 21,
  },

  authSwitchText: {
    color: "#8792A7",
    fontSize: 12,
  },

  authSwitchLink: {
    color: "#2457E6",
    fontSize: 12,
    fontWeight: "900",
  },

  authFooter: {
    color: "#A0ABC0",
    fontSize: 8,
    letterSpacing: 1.1,
    fontWeight: "800",
    textAlign: "center",
    marginTop: 30,
  },
});