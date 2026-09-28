<!-- preserved from https://blog.kscale.dev/we-are-here-for-the-long-haul-4ba400483a2b via https://web.archive.org/web/20240909135234id_/https://blog.kscale.dev/we-are-here-for-the-long-haul-4ba400483a2b -->

# We are here for the long haul

[![Paweł Budzianowski](https://miro.medium.com/v2/resize:fill:88:88/1*REeM2VDUPg7VWMU1UwnsBw.png)](https://medium.com/@budzianowski?source=post_page-----4ba400483a2b--------------------------------)[![K-Scale Labs](https://miro.medium.com/v2/resize:fill:48:48/1*MV_hSrOwtuWJWiHehtRsEg.png)](https://blog.kscale.dev/?source=post_page-----4ba400483a2b--------------------------------)

[Paweł Budzianowski](https://medium.com/@budzianowski?source=post_page-----4ba400483a2b--------------------------------)

·

[Follow](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fsubscribe%2Fuser%2F1681f4eee278&operation=register&redirect=https%3A%2F%2Fblog.kscale.dev%2Fwe-are-here-for-the-long-haul-4ba400483a2b&user=Pawe%C5%82+Budzianowski&userId=1681f4eee278&source=post_page-1681f4eee278----4ba400483a2b---------------------post_header-----------)

Published in

[K-Scale Labs](https://blog.kscale.dev/?source=post_page-----4ba400483a2b--------------------------------)

·

5 min read

·

Aug 9, 2024

--

Listen

Share

![]()

We believe the world will soon see an exponential increase in the number of useful and affordable humanoids deployed across labs, warehouses, and households worldwide. The price of hardware will soon drop below the cost of your favorite VR headset¹, and the AI software will become much more sophisticated and mature.

We also believe advancements in this field should be publicly accessible, which is why we created K-Scale Labs. The best part of building in the open-source spirit is sharing everything with the community instead of keeping it behind closed doors. With our updates, we want to share what we build and what we learn along the way.

# Laying the foundation

My co-founder Ben likes to say that the main reason GPT-2 was adopted faster and more widely than BERT is because you could immediately see the poetry it generated after training.² We are far from that setup in robotics, and K-Scale’s mission is to change that. In upcoming weeks we will share some updates on our affordable humanoidal platform that will open up new possibilities to roboticians, MLEs and enthusiasts so they can easily test new models and skills at home or lab.

In 2018, I collected the [largest task-oriented dialogue dataset](https://arxiv.org/abs/1810.00278) available to the community. 10,000 dialogues felt like more than enough (sic!), but the reality was that the foundation model was still missing. Just like in the NLP world, the robotics world is still searching for that foundation. And it feels like we’re making the same mistakes along the way. In the world of ubiquitous robots you still have to make them truly generalizable. We believe that achieving this is only possible being ML-first while fully hardware-aware.

We recognize the long road ahead in creating truly useful and widely adopted robots, but we’re excited to embrace the challenge and contribute to working towards a world where embodied intelligence is cheap, plentiful and useful.

# The data challenge: quality and diversity

Collecting the right data at scale is challenging, to put it mildly. There are two main issues with every collection: data quality and data diversity. Having spent a considerable portion of my ML career collecting conversational data, I believe you can’t escape these constraints, even with unlimited resources. Recent datasets like OXE, Droid (and many more) are fantastic steps forward, but the problem of quality will only become more challenging. Let’s look at some examples from the Droid dataset below:

The instruction is ‘Spread the jeans on the couch’.

The instruction is ‘Move the cup to the left and cover it’.

The ambiguity of the annotations is a major issue. With the challenges of the real world and the lack of a foundation model, any noise in the annotation, instead of helping the model generalize, will cause it to overfit to the noise. We will soon share our first datasets and tools to build initial filter models that can act as initial tests against incorrect annotations. Nevertheless, they will never be perfect.

Teleoperation feels like an obvious path, and most major robotics companies are taking it³. However, to use a well-worn analogy, it’s only the icing on the cake.

![]()

[Yann](https://noon99jaki.github.io/publication/2019-Lecun-Cake.pdf) Lecun Cake Analogy

We are quite skeptical of teleop as a solution since it distracts from focusing on the core of the problem. The harsh reality is that our “a lot” of data isn’t really that much, and data diversity will be a major bottleneck if we don’t have these robots in real-world environments. And just like in the NLP world, we try to collect vast amounts of data to train on specific tasks, incentivizing overfitting.

Playing around with raw teleoperation in the garage.

# Streamlining development

Dealing with CUDA issues when working on ML models is already frustrating. Adding to that world, ad-hoc URDF changes, different simulators with their quirks, and optimizing for sim-to-real makes ML robotics development a truly painful experience. That’s why we’re building tools to quickly go from CAD designs to modeling in your favorite simulator with URDF or XML files. All of this is shared at the [K-Scale Onshape library](https://github.com/kscalelabs/onshape).

We also want to help unify the simulation framework for modeling humanoid locomotion. Following [Humanoid Gym](https://github.com/roboterax/humanoid-gym) (and many other great community repositories), we’re building a broader sim-to-sim translation for our Stompy and other major humanoids like H1, G1, or GR-1. For more information, see [K-Scale Sim](https://github.com/kscalelabs/sim). We will also add more embodiments to [Isaac Lab](https://github.com/kscalelabs/isaaclab) to help the community easily test different models and ideas. With the recent acceleration of new designs and hardware deployments, the community will soon have an array of different humanoids of various sizes with an established protocol for cross-simulator tests.

# Modeling through simplicity

The [UMI](https://umi-gripper.github.io) and [Aloha](https://mobile-aloha.github.io/) projects popularized ACT and diffusion architectures. [IsaacLab](https://github.com/isaac-sim/IsaacLab), [LeRobot](https://github.com/huggingface/lerobot), and many other packages significantly lower the barrier to entry for newcomers to the field. Below, you can see a simple policy trained on a handful of examples, with the model generalizing to a new background.

New embodiment and a handful of dirty examples of pushing the can.

Training these skills is becoming a well-established and enjoyable process. This naturally leads us to the next step: multimodal models. The obvious trend will be to leverage pre-trained models that serve as good feature representations, and our community is already producing promising foundations like [OpenVLA](https://arxiv.org/abs/2406.09246). Just like with ACT, finetuned VLA works very well with our different embodiments.

However, just like a few years ago in NLP, we still talk about manipulation and locomotion separately. Just like we used to talk about parsing, dialogue, and summarization separately. Do you see the pattern? The development of the next generation of humanoids must be natively full-body and multimodal. This requires on-device support with low latency, capable of moving 16–20 joints in real-time. That’s why we are eager to share soon our larger models that build upon the latest developments in state-space models.

# Conclusions

There will be billions of autonomous, affordable, and helpful robots in the world, enabling us to do more productive and creative work. K-Scale Labs’ mission is to bring them to market at an affordable price with a simple software ecosystem where hardware and software are tightly integrated and driven by a single model.

To fulfill this dream, it seems the number of economic and research challenges is endless. If you feel you can help us tackle them, let us know! We’ve signed up for quite a long journey.

[1] If you don’t believe us just take a look at developments [here](https://www.youtube.com/watch?v=GzX1qOIO1bE) or [here](https://noetixrobotics.com) or [here](https://www.deeprobotics.cn/en) or dozens of other great labs.

[2] Even though the downstream performance doesn’t differ much between the pre-training tasks, see <https://arxiv.org/abs/2205.05131> .

[3] See how this works at the Tesla [factory](https://www.youtube.com/watch?v=OtpCyjQDW0w).
