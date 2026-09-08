> ## Documentation Index
> Fetch the complete documentation index at: https://wiki.agnes-ai.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Model Pricing

> List prices, current prices, and promotional billing rules for Agnes AI text, image, and video models on the international site.

This page summarizes the published USD prices for Agnes AI models on the international site. All prices are API prices; `M` means one million tokens.

<Info>
  “List price” is the standard price, while “current price” is the amount currently charged. Promotional end dates are subject to Agnes AI platform announcements and your account bill.
</Info>

## Text models

<table>
  <thead>
    <tr>
      <th>Model</th>
      <th>Billing item</th>
      <th>List price</th>
      <th>Current price</th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td rowSpan={2} style={{ verticalAlign: "middle" }}><code>agnes-2.0-flash</code><br /><strong>Deprecated</strong></td>
      <td>Input tokens</td>
      <td><del><code>\$0.03 / M</code></del></td>
      <td><strong><code>\$0 / M</code></strong></td>
    </tr>

    <tr>
      <td>Output tokens</td>
      <td><del><code>\$0.15 / M</code></del></td>
      <td><strong><code>\$0 / M</code></strong></td>
    </tr>

    <tr>
      <td rowSpan={2} style={{ verticalAlign: "middle" }}><code>agnes-2.5-flash</code></td>
      <td>Input tokens</td>
      <td><del><code>\$0.03 / M</code></del></td>
      <td><strong><code>\$0 / M</code></strong></td>
    </tr>

    <tr>
      <td>Output tokens</td>
      <td><del><code>\$0.15 / M</code></del></td>
      <td><strong><code>\$0 / M</code></strong></td>
    </tr>

    <tr>
      <td rowSpan={3} style={{ verticalAlign: "middle" }}><code>agnes-2.5-pro</code></td>
      <td>Cached input</td>
      <td><code>\$0.045 / M</code></td>
      <td><code>\$0.045 / M</code></td>
    </tr>

    <tr><td>Input tokens</td><td><code>\$0.45 / M</code></td><td><code>\$0.45 / M</code></td></tr>
    <tr><td>Output tokens</td><td><code>\$0.90 / M</code></td><td><code>\$0.90 / M</code></td></tr>

    <tr>
      <td rowSpan={3} style={{ verticalAlign: "middle" }}><code>agnes-2.5-pro-alpha</code><br /><strong>Deprecated</strong></td>
      <td>Cached input</td><td><code>\$0.045 / M</code></td><td><code>\$0.045 / M</code></td>
    </tr>

    <tr><td>Input tokens</td><td><code>\$0.45 / M</code></td><td><code>\$0.45 / M</code></td></tr>
    <tr><td>Output tokens</td><td><code>\$0.90 / M</code></td><td><code>\$0.90 / M</code></td></tr>

    <tr>
      <td rowSpan={3} style={{ verticalAlign: "middle" }}><code>agnes-2.5-pro-beta</code></td>
      <td>Cached input</td><td><code>\$0.01 / M</code></td><td><code>\$0.01 / M</code></td>
    </tr>

    <tr><td>Input tokens</td><td><code>\$0.10 / M</code></td><td><code>\$0.10 / M</code></td></tr>
    <tr><td>Output tokens</td><td><code>\$0.30 / M</code></td><td><code>\$0.30 / M</code></td></tr>
  </tbody>
</table>

### Current offers

* `agnes-2.0-flash` is deprecated; its prices are retained as historical records. Input and output tokens are currently free for `agnes-2.5-flash`.
* The hosted `agnes-2.5-pro-alpha` API is deprecated; its prices are retained as historical records. `agnes-2.5-pro` is billed at its published Pro-tier prices, while `agnes-2.5-pro-beta` uses the separate Beta prices shown above.

<Note>
  The cached-input price is 10% of the regular input-token price. It applies only to input tokens confirmed as cache hits by the service; all other input tokens use the regular input-token price.
</Note>

## Image models

<table>
  <thead>
    <tr><th>Model</th><th>Billing item</th><th>List price</th><th>Current price</th></tr>
  </thead>

  <tbody>
    <tr><td rowSpan={5} style={{ verticalAlign: "middle" }}><code>agnes-image-2.0-flash</code></td><td>1K output image</td><td><del><code>\$10 / 1,000 images</code></del></td><td><strong><code>\$0</code></strong></td></tr>
    <tr><td>2K output image</td><td><del><code>\$18 / 1,000 images</code></del></td><td><strong><code>\$0</code></strong></td></tr>
    <tr><td>3K output image</td><td><del><code>\$21 / 1,000 images</code></del></td><td><strong><code>\$0</code></strong></td></tr>
    <tr><td>4K output image</td><td><del><code>\$24 / 1,000 images</code></del></td><td><strong><code>\$0</code></strong></td></tr>
    <tr><td>Input reference images from the 4th onward</td><td><del><code>\$0.003 / image</code></del></td><td><strong><code>\$0 / image</code></strong></td></tr>
    <tr><td rowSpan={5} style={{ verticalAlign: "middle" }}><code>agnes-image-2.1-flash</code></td><td>1K output image</td><td><del><code>\$10 / 1,000 images</code></del></td><td><strong><code>\$0</code></strong></td></tr>
    <tr><td>2K output image</td><td><del><code>\$18 / 1,000 images</code></del></td><td><strong><code>\$0</code></strong></td></tr>
    <tr><td>3K output image</td><td><del><code>\$21 / 1,000 images</code></del></td><td><strong><code>\$0</code></strong></td></tr>
    <tr><td>4K output image</td><td><del><code>\$24 / 1,000 images</code></del></td><td><strong><code>\$0</code></strong></td></tr>
    <tr><td>Input reference images from the 4th onward</td><td><del><code>\$0.003 / image</code></del></td><td><strong><code>\$0 / image</code></strong></td></tr>
    <tr><td rowSpan={5} style={{ verticalAlign: "middle" }}><code>agnes-image-2.5-flash</code></td><td>1K output image</td><td><del><code>\$10 / 1,000 images</code></del></td><td><strong><code>\$0</code></strong></td></tr>
    <tr><td>2K output image</td><td><del><code>\$18 / 1,000 images</code></del></td><td><strong><code>\$0</code></strong></td></tr>
    <tr><td>3K output image</td><td><del><code>\$21 / 1,000 images</code></del></td><td><strong><code>\$0</code></strong></td></tr>
    <tr><td>4K output image</td><td><del><code>\$24 / 1,000 images</code></del></td><td><strong><code>\$0</code></strong></td></tr>
    <tr><td>Input reference images from the 4th onward</td><td><del><code>\$0.003 / image</code></del></td><td><strong><code>\$0 / image</code></strong></td></tr>
  </tbody>
</table>

### Current offer

`agnes-image-2.0-flash`, `agnes-image-2.1-flash`, and `agnes-image-2.5-flash` use the same prices and billing method. All output-resolution tiers and input reference images are currently free.

### Image list-price billing rule

At list price, output images are billed by resolution tier. For image-to-image and multi-image reference tasks, the first 3 input images do not incur an additional charge; each image from the 4th onward is billed separately.

```text theme={null}
List-price cost = output image count × output resolution unit price
                + max(0, input image count - 3) × $0.003
```

| Billing item                               | List price per image | Equivalent price per 1,000 output images |
| ------------------------------------------ | -------------------: | ---------------------------------------: |
| 1K output image                            |     `$0.010 / image` |                                    `$10` |
| 2K output image                            |     `$0.018 / image` |                                    `$18` |
| 3K output image                            |     `$0.021 / image` |                                    `$21` |
| 4K output image                            |     `$0.024 / image` |                                    `$24` |
| Input reference images from the 4th onward |     `$0.003 / image` |                           Not applicable |

### Current billing rule

The current price is `$0`: output images at every supported resolution tier are free, and input reference images—including the 4th and subsequent images—do not incur a charge.

## Video models

<table>
  <thead>
    <tr>
      <th>Model</th>
      <th>Billing item</th>
      <th>List price</th>
      <th>Current price</th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td><code>agnes-video-v2.0</code></td>
      <td>Video duration</td>
      <td><del><code>\$0.005 / second</code></del></td>
      <td><strong><code>\$0 / second</code></strong></td>
    </tr>

    <tr>
      <td rowSpan={5} style={{ verticalAlign: "middle" }}><code>agnes-video-2.5</code></td>
      <td>720P output video</td>
      <td><code>\$0.025 / second</code></td>
      <td><code>\$0.025 / second</code></td>
    </tr>

    <tr><td>1080P output video</td><td><code>\$0.040 / second</code></td><td><code>\$0.040 / second</code></td></tr>
    <tr><td>1K output video</td><td><code>\$0.040 / second</code></td><td><code>\$0.040 / second</code></td></tr>
    <tr><td>2K output video</td><td><code>\$0.055 / second</code></td><td><code>\$0.055 / second</code></td></tr>
    <tr><td>Input images from the 6th onward</td><td><code>\$0.005 / image</code></td><td><code>\$0.005 / image</code></td></tr>

    <tr>
      <td><code>agnes-video-2.5-flash</code></td>
      <td>720P video duration</td>
      <td><del><code>\$0.025 / second</code></del></td>
      <td><strong><code>\$0 / second</code></strong></td>
    </tr>
  </tbody>
</table>

### Current offers

* `agnes-video-v2.0` is currently free.
* `agnes-video-2.5` is billed by output resolution and total billable duration. Total billable duration is the sum of the output video duration and input video duration. The first 5 input images are free; each image from the 6th onward costs `$0.005`.
* `agnes-video-2.5-flash` uses the same billing formula as Agnes Video 2.5 and is currently free for a limited time.

### Agnes Video 2.5 and 2.5 Flash billing rule

```text theme={null}
Total video cost = output seconds × output resolution unit price
                 + input video seconds × output resolution unit price
                 + max(0, image count - free image allowance) × excess image unit price
```

| Billing item                     |        Unit price |
| -------------------------------- | ----------------: |
| 720P output video                | `$0.025 / second` |
| 1080P output video               | `$0.040 / second` |
| 1K output video                  | `$0.040 / second` |
| 2K output video                  | `$0.055 / second` |
| Input images from the 6th onward |  `$0.005 / image` |

Input video duration does not have a separate unit price, but it is included in total billable duration and charged at the selected output resolution rate.

For `agnes-video-2.5`, the free image allowance is 5 and the excess image unit price is `$0.005 / image`. `agnes-video-2.5-flash` follows the same list-price formula, but all of its current billing items are `$0` during the limited-time free promotion.

See [Agnes Video 2.5 billing](/en/docs/agnes-video-25#billing) for details.

## Billing notes

* Your Agnes AI account bill is the source of truth for actual charges.
* Current offers may vary by model, account eligibility, or promotion stage.
* Whether a failed request is billed depends on the final platform billing record.
* Price updates on this page will also be reflected in the corresponding model documentation.
