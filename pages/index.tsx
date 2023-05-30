import Head from "next/head";
import styles from "../styles/Home.module.css";

const Landing = () => {
  return (
    <div className={styles.container}>
      <Head>
        <title>Prop Betting</title>
        <meta
          name="description"
          content="Automatic Update Prop Lines and Suggested Bets"
        />
        <link rel="icon" href="/prophub.jpg" />
      </Head>

      <main className={styles.main}>
        <h1 className={styles.title}>Prop Hub</h1>
      </main>
    </div>
  );
};

export default Landing;
