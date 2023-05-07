import os
import openai
import ast
import requests
import time

from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

prompt_prefix = """You are the author of rekt.news, who has written all of the article content on rekt.news about hacks in the web3 space.

You have been tasked with classifying the type of attack (or attacks, if a single article discusses multiple categories in a single article) discussed in each of the rekt.news articles.

Here is an example, where the article text will be prefixed with "ARTICLE TEXT:\n" and the categories are a single array of string categories (each surrounded by double quotes):

ARTICLE TEXT:
$1.8M disappeared in a puff of smoke as Merlin pulled the classic DeFi magic trick.

Merlin, a DEX native to the recently-launched zksync L2, was in the middle of a 3-day “Liquidity Generation Event” as part of its token (MAGE) launch.

The alarm was initially raised by a community member before Peckshield spread the message. Merlin then acknowledged the incident, advising users to revoke permissions as a precaution.

Not to be confused with three-time leaderboard entrant Merlin Labs (who got rekt on repeat during Spring 2021's BSC bloodbath), Merlin had passed its second audit by Certik just two days before the attack.

Merlin's story may be that of a simple rug; a tale we've heard many times before.

But, this time, Merlin has inadvertently conjured a debate into the value of certain styles of audit…

Credit: BeosinAlert

The rug mechanism was a straightforward case of draining the liquidity pools into which users were depositing as part of the MAGE token sale.

This was made possible via max approvals granted to the Feeto address upon deployment of the pools. The individual/s in control of the Feeto address could then drain the pool of all assets, which were then bridged to ETH.

Merlin's own post-mortem places the blame squarely on the back-end development team. The thread includes links to developers' github profiles and states that Serbian authorities have been contacted.

The rugged funds were bridged back to Ethereum, swapped for ETH and transferred to other addresses.

Ruggers gonna rug.

And when many protocols have centralisation issues which could potentially lead to a rug, yet are overlooked by FOMO-ing apes and airdrop hunters…

Where does the blame really lie?
END

["rugpull"]

Here is another example of a rekt.news article (prefixed by "ARTICLE TEXT:\n") followed by the correct categories array:

ARTICLE TEXT:
Hundred Finance finally gets its very own article.

No sharing the spotlight this time…

Shortly after 2pm UTC on April 15th, Hundred Finance suffered a $7.4M exploit on Optimism.

The team's announcement sounded more like a bystander's observation than a protocol informing users of a multimillion dollar hack…

It looks that Hundred got hacked on #Optimism. We will update when there is more information to it.

But, then again, Hundred have been through all this before.

Last February, Hundred caught a stray to the tune of 3.3M when Meter got rekt.

The following month saw Hundred's leaderboard debut, when $6.2M was lost on xDAI chain to a dual-edged attack which also hit Agave DAO for $5.5M.

That time, the attack vector was the same reentrancy mechanism which hit CREAM Finance in August 2021.

With Hundred's leaderboard total now standing at $16.9M…

…what was it this time?

Credit: Daniel Von Fange, Peckshield, Beosin, Numen Cyber

Hundred is a Compound fork which uses hTokens to track lending positions. It was audited in Feb 2022 by WhiteHatDAO.

As Daniel Von Fange points out:

the project setup two wBTC cTokens, one of which was used by the UI, one of which was empty.

Using a flashloan of WBTC from Aave, the attacker was able to donate large amounts of WBTC to the empty hWBTC contract, manipulating the exchange rate between hWBTC and WBTC. To top it off, the redeemUnderlying function contained a rounding error.

Attacker's address (OP, ETH): 0x155da45d374a286d383839b1ef27567a15e67528

Hack tx 1: 0x6e9ebcde…

Hack tx 2: 0x15096dc6…

Peckshield summed up the exploit as:

The root cause appears the attacker donates 200 WBTC to inflate hWBTC's exchange rate so that even a tiny amount (2 wei) of hWBTC can basically drain current lending pools.

Beosin also provided a step-by-step analysis:

The root cause is that the attacker can manipulate the exchangeRate by donating a large amount of WBTC to the hWBTC contract.

In the getAccountSnapshot function, the value of exchangeRateMantissa relies on the amount of WBTC in the contract.

The attacker flashloaned 500 $WBTC, then called the redeem function to redeem the previously staked 0.3 WBTC.

Next, the attack contract 1 sent 500.3 WBTC to attack contract 2. Contract 2 used 4 BTC to mint 200 hWBTC. The redeem function was then called to redeem the 4 BTC.

Here the attacker can redeem the 4 WBTC previously staked with less than 200 hWBTC. At this point the attacker had a very small amount of hWBTC left on contract 2.

Attack contract 2 then sent 500.3 WBTC to the hWBTC contract and borrowed 1021.91 ETH via the remaining 2 hWBTCs.

Finally the attack contract 2 repaid the previous debt by using 1 hWBTC, and withdrew 500.3 WBTC from the contract.

The attacker bridged most of the stolen funds to ETH where centralised stables USDT and USDC were swapped, or deposited into Curve.

At the time of writing, the hacker's debank profile shows approximately $5.4M of assets on Ethereum and $0.9M remaining on Optimism.

The price of HND token dropped around 50% over the day following the hack. It has since recovered somewhat, to ~$0.025, down from ~$0.039 before the attack.

As we wrote last time:

Forks upon forks create a house of cards. If the code is copied and pasted, vulnerabilities can open up where they're least expected.

When one fork falls, all others have to check their foundations.

Hundred have advised other COMP forks to get in touch, warning that the hack exploited “a general flaw in the code and not specific to Hundred deployment”.

Likely spurred on by Euler Finance's recent success, the Hundred team have announced a reward for info leading to identification of the hacker:

48h passed since we sent an on-chain message to the hacker and tried to start negotiations with him.

Today we are launching a $500k reward in the hope that this provides additional incentive for info that leads to the Hundred attacker's arrest and the return of all funds.

Hopefully the added pressure is as effective in recovering the funds…

Will Hundred get lucky?
END

["flashloan_exploit", "contract_manipulation", "reentrancy_attack"]

Here is one last example of article followed by the categories:

ARTICLE TEXT:
rekt in prod.

…eventually.

Over two years since its first leaderboard entry, Yearn has landed back on rekt.news having lost over $10M.

Considered by many as one of DeFi's most reliable, secure platforms, Yearn made it's name by offering some of the sector's simplest farming opportunities.

The immutable yUSDT contract that was attacked was deployed over three years ago, back when Yearn was Andre Cronje's iearn finance.

While the strategy was superceded by newer versions, plenty of funds still remained in the original contract. Later Yearn vault contracts are not affected.

Despite a last-minute warning on Twitter, immutable contracts can't be saved.

Team member storming0x acknowledged the attack before Yearn reassured users that current contracts were unaffected.

1156 days to spot a multimillion dollar vulnerability in one of DeFi's longest established protocols.

How did it take so long?

Credit: Samczsun, OtterSec, SlowMist

The attacker exploited a misconfiguration in the iearn yUSDT token contract.

The token generated yield via an underlying basket of yield-bearing tokens, including USDT positions on Aave, Compound, DYDX and BzX's Fulcrum.

However, since launch, the yUSDT has contained what appears to be a copy/paste error whereby the Fulcrum USDC address was used instead of the Fulcrum USDT contract.

The exploiter was able to take advantage of the misconfiguration to vastly manipulate the underlying share prices of yUSDT, and mint a large quantity (1.2 quadrillion) of yUSDT using just 10k USDT.

Theori's junomon.eth provided the step-by-step analysis:

Exploiter address 1: 0x5bac20beef31d0eccb369a33514831ed8e9cdfe0

Exploiter address 2: 0x16af29b7efbf019ef30aae9023a5140c012374a5

Exploiter address 3: 0x6f4a6262d06272c8b2e00ce75e76d84b9d6f6ab8

Attack transaction 1: 0xd55e43c1…

Attack transaction 2: 0x8db0ef33…

The minted yUSDT was then swapped for other stables totalling $11.4M, BlockSec provided the following breakdown:

The attacker was funded via Tornado Cash and redeposited 1000 ETH for laundering. At the time of writing, the first two exploiter addresses contain approximately $1.5M of assets each, and address 3 contains 7.4M DAI.

Certik conducted an audit of iearn finance in Feb 2020, however it appears that only the yDAI contract was investigated.

The test in prod attitude, Cronje's preferred method, has been responsible for plenty of incidents, providing much of rekt.news' early content.

Generally, though, new protocols and features got rekt within hours or days, not years…

In the wake of each attack, a decentralised monopoly began to grow.

The wider Cronje-verse has experienced enough incidents to have its own leaderboard, as we discussed after CREAM Finance was hacked for the second time, in October 2021.

Despite the significant losses, it's lucky that this case only affected an old and deprecated strategy, and didn't threaten the $450M of TVL across current Yearn strategies.

As we wrote last time:

No protocol is too big to fail.

First Sushi, now Yearn.

It's a big week for DeFi stalwarts getting rekt.

Who will be next?
END

["misconfiguration_exploit", "contract_manipulation"]

Now, I want you to summarize the following article, which will be prefixed with "ARTICLE TEXT:\n" and end with "END\n", and I want you to take the category dictionary into account when choosing the category array for this article. The categories will be a Python dict enclose by "---" before and after. In yoru answer I want you to respond with a single array of string categories (surrounded by double quotes):

ARTICLE TEXT:
{markdown}
END

---
{old_categories}
---
"""

def infer_categories_from_article(markdown, old_categories):

    # infer categories for this article from OpenAI API
    prompt = prompt_prefix.format(markdown=markdown, old_categories=old_categories)
    resp = {}

    counter = 0

    while True:
        if counter >= 3:
            # we've tried 3 times, let's just give up
            raise Exception("Something is wrong with openai, timing out")
        try:
            resp = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
            )
            break
        except requests.exceptions.RequestException as e:
            print(f"OPENAI Error: {e}")
            time.sleep(20)
            counter = counter + 1

    if not resp.choices or len(resp.choices) != 1:
        print(f"ERROR: {resp}")
        raise Exception("unexpected response from OpenAI API")

    # convert string ["rugpull"] to an actual Python list
    categories_as_string = resp.choices[0].message.content
    new_categories = ast.literal_eval(categories_as_string)
    if new_categories is None:
        raise Exception(f"unable to parse categories string {categories_as_string}")
    if len(new_categories) != len(set(new_categories)):
        raise Exception(f"categories {new_categories} contain duplicates")

    return new_categories